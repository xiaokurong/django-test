from django.shortcuts import render
# from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from . import saltapi



def index(request):
    return HttpResponse('hello,world!')

def saltapicmd(request):
    if request.method == 'POST':
        hostnames=request.POST.get('hostnames')
        commands=request.POST.get('commands')
        try:
            sapi=saltapi.SaltAPI(url='https//172.20.20.70:8000',username='saltapi',password='saltapi')
            salt_client=hostnames
            salt_method='cmd.run'
            salt_params = commands
            reinfos = sapi.salt_command(salt_client,salt_method,salt_params)
            return render(request,'saltapi/saltapirun.html',{'login_err': reinfos})
        except Exception:
            return render(request,'saltapi/saltapirun.html',{'login_err': 'error'})

    else:
        return render(request,'saltapi/saltapirun.html')


