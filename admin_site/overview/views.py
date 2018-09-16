from django.shortcuts import render
from django.http import Http404
import requests
import json
# Create your views here.


def index(request):
    r = requests.get('http://dms_server:5000/apps')

    apps = [ app_json['id'] for app_json in r.json() ]
    context = {
        'apps_list': apps if r.status_code == 200 else []
    }
    return render(request, 'overview/index.html', context)


def detail(request, app_id):

    r = requests.get('http://dms_server:5000/entries/{}'.format(app_id))

    entries = [ entry['data'] for entry in r.json() ]

    context = {
        'app_entry_list': entries
    }

    return render(request, 'overview/detail.html', context)