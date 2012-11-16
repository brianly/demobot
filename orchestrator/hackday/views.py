# Create your views here.
from django.http import HttpResponse
#from django.shortcuts import render_to_response
#from django.views.decorators.http import require_http_methods
#
#from hackday.models import Poll
try:
     import json
except ImportError:
     import simplejson as json


def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")

def detail(request, poll_id):
    return HttpResponse("You're looking at poll %s." % poll_id)

def results(request, poll_id):
    return HttpResponse("You're looking at the results of poll %s." % poll_id)

def vote(request, poll_id):
    return HttpResponse("You're voting on poll %s." % poll_id)

#@require_http_methods(['POST'])
#def event(request, event):
#    d = {'success': 5,
#         '6': 7}
#
#    return HttpResponse(event, content_type='application/json')


