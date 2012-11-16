from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from hackday.models import Event, Post


class EventResource(ModelResource):
    """Events are triggers to start execution of tasks"""
    class Meta:
        queryset = Event.objects.all()
        resource_name = 'event'
        authorization= Authorization()

class PostResource(ModelResource):
    """Posts are individual objects in Yammer"""
    class Meta:
        queryset = Post.objects.all()
        resource_name = 'post'
        authorization= Authorization()
