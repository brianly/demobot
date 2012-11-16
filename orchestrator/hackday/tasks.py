from celery import task
from time import sleep
from hackday.models import Script, Post, Thread, Log
import requests
import sys

try:
    import json
except ImportError:
    import simplejson as json

def _oauth_header(token):
    return {"Authorization": "Bearer %s" % token}

def post_thread_starter(post, group_id):
    base_url = 'https://www.yammer.com/api/v1/'
    config = {}#{'verbose': sys.stderr}
    endpoint = 'messages'
    url = '%s%s%s' % (base_url, endpoint, '.json')

    payload = {'body': post.content, 'group_id': group_id}

    # Post the thread starter
    r = requests.post(url, headers=_oauth_header(post.token), params=payload, config=config)
    resp = r.json

    # Get the fucking thread starter
    refs = resp['references'][0]
    tsi = refs['thread_starter_id']

    log1 = Log()
    log1.message_id = tsi
    log1.save()

    sleep(post.delay)

    return tsi

def post_reply(post, group_id, reply_to_id):
    base_url = 'https://www.yammer.com/api/v1/'
    config = {} # {'verbose': sys.stderr}
    endpoint = 'messages'
    url = '%s%s%s' % (base_url, endpoint, '.json')

    payload = {'body': post.content, 'group_id': group_id, 'replied_to_id': reply_to_id}

    # Post the thread starter
    r = requests.post(url, headers=_oauth_header(post.token), params=payload, config=config)


    resp = r.json
    msgd = resp['messages'][0]
    pid = msgd['id']
    log2 = Log()
    log2.message_id = pid
    log2.save()

    sleep(post.delay)

    pass

class ThreadContainer(object):

    def __init__(self, name, group_id):
        self.name = name
        self.group_id = group_id
        self.thread_starter = []
        self.replies = []

    def add_starter(self, ts):
        if ts is None:
            print 'error'
        self.thread_starter.append(ts)

    def add_reply(self, reply):
        self.replies.append(reply)

    def __unicode__(self):
        return '%s (items %s)' % (self.thread_starter, len(self.replies))

    def __str__(self):
        return '%s (items %s)' % (self.thread_starter, len(self.replies))


def build_posts2(thread):
    ordered_posts = []

    posts = Post.objects.filter(thread__name=thread.name).all().order_by('-is_starter')

    for post in posts:
        ordered_posts.append(post)

    return ordered_posts

@task()
def start(event_name):
    print "Starting to process: %s" % event_name

    threads = Thread.objects.filter(script__name=event_name).all()

    threads_to_post_as_class = []

    # build the threads
    for thread in threads:
        posts1 = build_posts2(thread)
        thr = ThreadContainer(thread.name, thread.group_id)

        for k, v in enumerate(posts1):
            if v.is_starter:
                thr.add_starter(v)
            else:
                thr.add_reply(v)
            print

        threads_to_post_as_class.append(thr)

    # post stuff
    for t in threads_to_post_as_class:
        if len(t.thread_starter) > 0:
            ts = t.thread_starter[0]
            print '%s\t%s\t%s' % (ts.is_starter, ts.content, ts.token)

            tsi = post_thread_starter(ts, t.group_id)

            for reply in t.replies:
                print '%s\t%s\t%s\t%s' % (reply.is_starter, reply.content, reply.token, tsi)
                post_reply(reply, t.group_id, tsi)

    return len(threads_to_post_as_class)





@task()
def add(x, y):
    # sleep(400)
    return x + y
