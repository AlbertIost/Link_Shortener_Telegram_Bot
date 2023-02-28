import re

from django.views.decorators.csrf import csrf_exempt

from ugc.models import Link
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .utils import *
# Create your views here.

def click_on_short_link(request, link_token):
    crawlers = [
        'google', 'yandex', 'baiduspider', 'lycos', 'genieo', 'slurp', 'webalta', 'facebook',
        'mail.Ru', 'ia_archiver', 'teoma', 'yahoo', 'ask', 'rambler', 'crawler4j', 'mj12',
        'seznam', 'bot', 'curl', 'duckduckgo', 'aol', 'lighthouse', 'telegram'
    ]
    pattern = '|'.join(crawlers)
    try:
        link = Link.objects.get(token=link_token)
        response = redirect(link.original_link)

        if not re.search(pattern, str(request.META['HTTP_USER_AGENT']).lower()):
            register_click_on_link(link, get_client_ip(request))

        return response
    except:
        return HttpResponseNotFound('Link not found')
