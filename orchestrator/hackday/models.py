from django.db import models

class Script(models.Model):
    name = models.CharField(max_length=15, unique=True)
    description = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Thread(models.Model):
    script = models.ForeignKey(Script)
    name = models.CharField(max_length=15, unique=True)
    description = models.CharField(max_length=50)
    group_id = models.IntegerField()

    def __unicode__(self):
        return self.name


class Post(models.Model):
    thread = models.ForeignKey(Thread)
    is_starter = models.BooleanField()
    name = models.CharField(max_length=15, unique=True)
    content = models.CharField(max_length=9000)
    metadata = models.CharField(max_length=9000)
    token = models.CharField(max_length=50)
    delay = models.IntegerField()

    def __unicode__(self):
        return '%s (%s / %s)' % (self.name, self.thread.name, self.thread.script.name)


#    * Message content
#    * OG metadata
#    * Group ID, if not main feed.
#    * OAuth token for user
#    * Delay in seconds (optional - posts are always delayed a bit to avoid rate limits)

class Event(models.Model):
    """An incoming event that we need to start processing"""
    name = models.CharField(max_length=20)

def event_post_save(sender, instance, signal, *args, **kwargs):
    """Starts a Task when an Event is created"""
    from hackday.tasks import start

    print 'Received "%s" for processing' % (instance.name)
    start.delay(instance.name)

# Wire up the post_save handler for Events
models.signals.post_save.connect(event_post_save, sender=Event)



class Log(models.Model):
    message_id = models.CharField(max_length=50)















class Playbook(models.Model):
    name = models.CharField(max_length=20)

class Act(models.Model):
    playbook = models.ForeignKey(Playbook)
    name = models.CharField(max_length=20)

class Line(models.Model):
    act = models.ForeignKey(Act)
    name = models.CharField(max_length=20)
    # token = ""
    # action = ""
    # delay = 10
    # in_reply_to = "" # optional


class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()

    def __unicode__(self):
        return self.choice
