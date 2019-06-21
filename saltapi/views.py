from django.shortcuts import render, redirect
# from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from . import saltapi
from .models import ServerInfo,UserInfo,UserPriv,ServerGroup, OffenCommand
from collections import defaultdict



def index(request):

    return render(request,'saltapi/home.html',{'welcome': 'salt index'})


def brief(request):
    return render(request,'saltapi/brief.html',)

def saltapicmd(request):
    if request.method == 'POST':
        hostnames=request.POST.get('hostnames')
        commands=request.POST.get('commands')

        try:
            sapi=saltapi.SaltAPI(url='https://172.20.20.70:8000/',username='saltapi',password='saltapi')
            salt_client=hostnames
            salt_method='cmd.run'
            salt_params = commands
            reinfos = sapi.salt_command(salt_client,salt_method,salt_params)
            OffenCommand.objects.create(command_name=commands, hostnames=hostnames,command_result=reinfos)
            return render(request,'saltapi/saltapirun.html',{'login_err': reinfos})
        except Exception as error:
            return render(request,'saltapi/saltapirun.html',{'login_err': error})

    else:
        return render(request,'saltapi/saltapirun.html')

def history(request):
    try:
        history_set = OffenCommand.objects.all()
        return render(request, 'saltapi/history.html', {"history_set": history_set})
    except Exception as error:
        return  render(request,'saltapi/history.html',{"error": error})




def server(request):

    try:
        server_set = ServerInfo.objects.all()

    except ServerInfo.DoesNotExist:
        render(request,'saltapi/server.html',{'server_set': server_set, })


    return render(request,'saltapi/server.html',{'server_set': server_set,})

def servergroup(request):
    try:
        server_group_set = ServerGroup.objects.all()
        return render(request, 'saltapi/servergroup.html', {'server_group_set': server_group_set, })
    except Exception as error:
        return render(request,'saltapi/servergroup.html',{'error': error})



def user(request):
    try:
        user_set = UserInfo.objects.all()
    except UserInfo.DoesNotExist:
        render(request,'saltapi/user.html',{'user_set': user_set,})
    return render(request,'saltapi/user.html',{'user_set': user_set})

def other(request):
    return render(request,'saltapi/other.html',)

def insert(request):
    if request.method == 'POST':
        salt_name = request.POST['salt_name']
        server_name = request.POST['server_name']
        cpu = request.POST['cpu']
        cpu_core = request.POST['cpu_core']
        system = request.POST['system']
        ip_addr = request.POST['ip_addr']
        ram = request.POST['ram']
        disk = request.POST['disk']


        ServerInfo.objects.create(salt_name=salt_name,server_name=server_name,cpu=cpu,cpu_core=cpu_core,system=system,ip_addr=ip_addr,ram=ram,disk=disk)

    else:
        return render(request,'saltapi/insert.html')

    return render(request,'saltapi/insert.html',{'insert': '添加成功。'})


def refresh(request):
    try:
        gsapi = saltapi.SaltAPI(url='https://172.20.20.70:8000/', username='saltapi', password='saltapi')
        gsalt_client = '*'
        gsalt_method = 'grains.items'
        all_list= defaultdict(dict)

        all_grains = gsapi.salt_command(gsalt_client, gsalt_method)

    #     return render(request, 'saltapi/refresh.html', {'all_grains': all_grains,})
    # except Exception as error:
    #     render(request,'saltapi/refresh.html',{'refresh': error})
    #     print(all_grains)

        # for i in all_grains.keys():
        #     all_list[i]['salt_name']= all_grains[i]['id']
        #     all_list[i]['server_name'] = all_grains[i]['nodename']
        #     all_list[i]['cpu'] = all_grains[i]['cpu_model']
        #     all_list[i]['cpu_core'] = all_grains[i]['num_cpus']
        #     all_list[i]['system'] = all_grains[i]['os'] + ' ' + all_grains[i]['osrelease']
        #     all_list[i]['ip_addr'] = str(all_grains[i]['ipv4']).replace("'127.0.0.1',","")
        #     all_list[i]['ram'] = all_grains[i]['mem_total']
        #     # disk_all=gsapi.salt_command(all_grains[i]['id'],'disk.usage')
        #     # all_disk=0
        #     # for j in disk_all.keys():
        #     #     all_disk += disk_all[j]['available']
        #     #
        #     # all_list[i]['disk']=all_disk
        # print("************************************************")
        # print(all_list)
        # print("************************************************")
        return render(request, 'saltapi/refresh.html', {'all_grains': all_grains, })

    except Exception as error:
        return render(request, 'saltapi/refresh.html', {'refresh_error': error})

def serverchange(request,server_id):

    if request.method == 'GET':
        change_set = ServerInfo.objects.get(id=server_id)
        group_set = ServerGroup.objects.all()
        return render(request,'saltapi/serverchange.html',{'change_set': change_set,'group_set': group_set})
    else:
        salt_name = request.POST.get('salt_name')
        server_name = request.POST.get('server_name')
        cpu = request.POST.get('cpu')
        cpu_core = request.POST.get('cpu_core')
        system = request.POST.get('system')
        ip_addr = request.POST.get('ip_addr')
        ram = request.POST.get('ram')
        add_date = request.POST.get('add_data')
        group_id = request.POST.get('group_id')

        update_set = ServerInfo.objects.get(id=server_id)
        update_set.salt_name = salt_name
        update_set.server_name = server_name
        update_set.cpu = cpu
        update_set.cpu_core = cpu_core
        update_set.system = system
        update_set.ip_addr = ip_addr
        update_set.ram = ram
        update_set.add_date = add_date
        update_set.group_id = group_id
        update_set.save()
        return redirect('server')







