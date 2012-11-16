from celery import task
from time import sleep
from hackday.models import Script, Post, Thread
import requests
import sys

try:
    import json
except ImportError:
    import simplejson as json

def _oauth_header(token):
    return {"Authorization": "Bearer %s" % token}

def build_posts(thread):
    ordered_posts = []

    posts = Post.objects.filter(thread__name=thread.name).all().order_by('-is_starter')

    for post in posts:
        ordered_posts.append(post)

    return ordered_posts

def post_thread(thread, group_id):
    base_url = 'https://www.yammer.com/api/v1/'
    config = {'verbose': sys.stderr}
    endpoint = 'messages'
    url = '%s%s%s' % (base_url, endpoint, '.json')

    if len(thread) > 0:

        post = thread[0]
        payload = {'body': post.content, 'group_id': group_id}

        # Post the thread starter
        r = requests.post(url, headers=_oauth_header(post.token), params=payload, config=config)
        resp = r.json

        # Get the fucking thread starter
        refs = resp['references'][0]
        tsi = refs['thread_starter_id']
        print tsi

        sleep(post.delay)

#        # Use the thread starter ID for the other posts
        for k, v in enumerate(thread):
            if k > 0:
                post = v
                print 'key %s' % k
                payload['replied_to_id'] = tsi # Add to the query string
                r = requests.post(url, headers=_oauth_header(post.token), params=payload, config=config)
    #            print r.text

                sleep(post.delay)


@task()
def add(x, y):
    # sleep(400)
    return x + y

@task()
def start(event_name):
    print "Starting to process: %s" % event_name

    threads = Thread.objects.filter(script__name=event_name).all()

    threads_to_post = []
    for thread in threads:
        t = {
            'posts': build_posts(thread),
            'group_id': thread.group_id
        }
        threads_to_post.append(t)
#        threads_to_post.append(build_posts(thread))

    for t in threads_to_post:
        post_thread(t['posts'], t['group_id'])
        print t

    return threads.count()
