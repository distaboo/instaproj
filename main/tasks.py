from background_task import background
import time
import re
from main.models import *
from InstagramAPI import InstagramAPI

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

@background(schedule=1)
def parsing(id):
    pars = Parsing.objects.get(pk=1)
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
            try:
                t = apiswork[n].getUsernameInfo(k['pk'])
                lj = apiswork[n].LastJson['user']
            except:
                pass
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


