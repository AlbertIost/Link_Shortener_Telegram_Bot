from django.views.decorators.csrf import csrf_exempt

from ugc.models import Link
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .utils import *
# Create your views here.

def click_on_short_link(request, link_token):
    try:
        link = Link.objects.get(token=link_token)
        response = redirect(link.original_link)

        register_click_on_link(link, get_client_ip(request))

        return response
    except:
        return HttpResponseNotFound('Link not found')
