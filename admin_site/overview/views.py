from django.shortcuts import render
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
