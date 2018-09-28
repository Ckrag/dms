import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import App
from .models import Stat


# Create your views here.


def index(request):
    r = requests.get('http://dms_server:5000/apps')

    apps = [app_json['id'] for app_json in r.json()]
    context = {
        'apps_list': apps if r.status_code == 200 else []
    }
    return render(request, 'overview/index.html', context)


def detail(request, app_id):
    r = requests.get('http://dms_server:5000/entries/{}'.format(app_id))

    entries = [entry['data'] for entry in r.json()]

    context = {
        'app_entry_list': entries
    }

    return render(request, 'overview/detail.html', context)


@csrf_exempt
def save_app_config(request):
    app = request.POST['app']
    prop = request.POST['prop']
    path = request.POST['path']

    stat = Stat.objects.get_or_create(path=path, name=prop)
    app = App.objects.get_or_create(stat=stat, name=app)
    app.save()

    return HttpResponse(status=200)
