from django.shortcuts import render
from main.forms import *
from main.models import *
from InstagramAPI import InstagramAPI
import requests
import time
from threading import Thread
from django.shortcuts import redirect
import re
import os
from django.conf import settings
from django.http import HttpResponse, Http404

pars = Parsing.objects.get(pk = 1)
usernames = Acc.objects.values_list('username')
passwords = Acc.objects.values_list('password')
curname = ''
apis = []
apiswork = []
countEmail = 0
countBioEmail = 0
counter = 0
def cnt(n):
    for i in range(n):
            global counter
            counter = counter + 1
            time.sleep(1)
            print(counter)

thread = Thread(target=cnt)
thread.daemon = True
#thread.start()
for u,p in zip(usernames, passwords):
    apis.append(InstagramAPI(u[0],p[0]))

    print('nhey')
#api = InstagramAPI("willseerussianparadise", "xflava13")
print(usernames)
def apiLogin(api,user):
    if (api.login()):
        #api.getSelfUserFeed()  # get self user feed
        #print(api.LastJson)  # print last response JSON
        apiswork.append(api)
        print("Login succes {}!".format(user[0]))
    else:
        print("Can't login {}!".format(user[0]))
        #apis.remove(api)


for a , u in zip(apis,usernames):
    print(a)
    print('nhey')
    time.sleep(3)
    #api = InstagramAPI(a[0],a[1])
    apiLogin(a,u)


def parsing(id):
    pars.currentState = True
    foll = apiswork[0].getTotalFollowings(id)
    pars.currentTotal = len(foll)
    pars.save()
    i = 0
    sum = []
    sumBio = []
    l = len(apiswork)
    for k in foll:
        if pars.currentState == True:
            n = i % l
            print(i)
            i = i + 1
            pars.currentVar = i
            pars.save()
            time.sleep(3/l/2)
            t = apiswork[n].getUsernameInfo(k['pk'])
            lj = apiswork[n].LastJson['user']
            global countBioEmail
            global countEmail
            try:
                b = lj['biography']
                e = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", b)
                if not (len(e)==0):sumBio.append(e[0])
                countBioEmail = len(sumBio)
            except:
                pass
            try:
                e = lj['public_email']
                #print(lj)
                if not (len(e)==0):sum.append(e)
                #print(apiswork[n].LastJson['user']['public_email'])
                countEmail = len(sum)
            except:
                pass
        else:
            break
    pars.info = 'Парсинг {} завершен'.format(curname)
    pars.currentState = False
    pars.result = str(sum)
    pars.save()

    f = open('listButton.txt', 'w')
    f.write("\n".join(sum))
    f.close()

    fb = open('list.txt', 'w')
    fb.write("\n".join(sumBio))
    print(sumBio)
    fb.close()



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

    if pars.currentState == False:
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = IdForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                global curname
                global countEmail
                global countBioEmail
                curname = request.POST['insid']
                try:
                    id = getID(curname)
                except:
                    pars.info = 'Некорректный логин: {}'.format(curname)
                    return redirect('/')
                global thread
                thread = Thread(target=parsing, args=(id,))
                thread.daemon = True
                thread.start()
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