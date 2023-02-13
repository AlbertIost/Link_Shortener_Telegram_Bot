from django.views.decorators.csrf import csrf_exempt

from ugc.models import Link
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
# Create your views here.


@csrf_exempt
def webhook(request):
    if request.content_type == 'application/json':
        return HttpResponse('hello')
    else:
        return HttpResponse('no hello')


def short_link(request, link_token):
    try:
        link = Link.objects.get(token=link_token)
        response = redirect(link.original_link)
        return response
    except:
        return HttpResponseNotFound('Link not 2323 323223 found')
