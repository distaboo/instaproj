from django.shortcuts import render
from main.forms import *
from main.models import *
from InstagramAPI import InstagramAPI
import requests
import time
from threading import Thread
from django.shortcuts import redirect

import os
from django.conf import settings
from django.http import HttpResponse, Http404

from main.tasks import parsing


curname = ''
countEmail = ''
countBioEmail = ''



pars = Parsing.objects.get(pk = 1)

def download(request, path):
    file_path =  path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def getID(name):
    r = requests.get('https://www.instagram.com/'+name+'/?__a=1')
    return r.json()['logging_page_id'][12:]

def index(request):
    pars = Parsing.objects.get(pk=1)

    context = {
        'total': pars.currentTotal,
        'var': pars.currentVar,
        'countBioEmail': countBioEmail,
        'countEmail': countEmail,
        'info': pars.info,
        'name': curname,

    }

    return render(request, 'index.html', context=context)
# Create your views here.
def start(request):
    # if this is a POST request we need to process the form data
    print('13')
    if pars.currentState == False:
        print('13')
        if request.method == 'POST':
            print('13')
            # create a form instance and populate it with data from the request:
            form = IdForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                print('13')
                global curname
                global countEmail
                global countBioEmail
                print('13')
                curname = request.POST['insid']
                try:
                    id = getID(curname)
                except:
                    pars.info = 'Некорректный логин: {}'.format(curname)
                    return redirect('/')

                #thread = Thread(target=parsing, args=(id,))
                #thread.daemon = True
                #thread.start()
                print(id)
                parsing(id)
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                countEmail = 0
                countBioEmail = 0

                pars.info = 'Парсер работает с {}'.format(curname)
                pars.currentVar = 0
                pars.currentTotal = 0

                pars.save()
                return redirect('/')
    pars.info = 'Парсер уже работает с {}'.format(curname)
    pars.save()
    return redirect('/')

def stop(request):
    pars.info = 'Парсинг {} остановлен'.format(curname)
    pars.currentState = False
    pars.save()

    return redirect('/')