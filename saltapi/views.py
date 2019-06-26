from django.shortcuts import render, redirect
# from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from . import saltapi
from .models import ServerInfo,UserInfo,UserPriv,ServerGroup, OffenCommand
from collections import defaultdict



def index(request):

    return render(request,'saltapi/home.html',{'welcome': 'salt index'})

#首页
def brief(request):
    return render(request,'saltapi/brief.html',)

#salt命令执行
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

#查询历史命令
def history(request):
    try:
        history_set = OffenCommand.objects.all()
        return render(request, 'saltapi/history.html', {"history_set": history_set})
    except Exception as error:
        return  render(request,'saltapi/history.html',{"error": error})



#查询服务器信息
def server(request):

    try:
        server_set = ServerInfo.objects.all()
        group_set = ServerGroup.objects.all()
        return render(request,'saltapi/server.html',{'server_set': server_set,'group_set': group_set})

    except ServerInfo.DoesNotExist:
        render(request,'saltapi/server.html',{'server_set': server_set, })


#查询服务器分组信息
def servergroup(request):
    try:
        server_group_set = ServerGroup.objects.all()
        server_set = ServerInfo.objects.all()
        return render(request, 'saltapi/servergroup.html', {'server_group_set': server_group_set, 'server_set': server_set})
    except Exception as error:
        return render(request,'saltapi/servergroup.html',{'error': error})

#修改服务器分组
def servergroup_change(request,group_id):
    if request.method == 'GET':
        group = ServerGroup.objects.get(id=group_id)
        return render(request,'saltapi/servergroup_change.html',{'group': group })
    else:
        group = ServerGroup.objects.get(id=group_id)
        groupname = request.POST.get('group_name')
        groupcomment = request.POST.get('comment')
        group.group_name = groupname
        group.comment = groupcomment
        group.save()
        return redirect('/saltapi/servergroup')

#添加服务器分组
def servergroup_add(request):
    if request.method == 'GET':
        return render(request,'saltapi/servergroup_add.html',)
    else:
        groupname = request.POST.get('group_name')
        groupcomment = request.POST.get('comment')
        ServerGroup.objects.create(group_name = groupname,comment=groupcomment)
        return redirect('/saltapi/servergroup')


#删除服务器分组
def servergroup_del(request,group_id):
    group = ServerGroup.objects.get(id=group_id)
    group.delete()
    return redirect('/saltapi/servergroup')

def other(request):
    return render(request,'saltapi/other.html',)

#新增服务器信息
def serveradd(request):
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
        return render(request,'saltapi/serveradd.html')

    return render(request,'saltapi/serveradd.html',{'serveradd': '添加成功。'})

#刷新salt-stack所有客户端
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

#修改服务器信息
def serverchange(request, server_id):

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
        add_date = request.POST.get('add_date')
        group_id = request.POST.get('group_id')

        update_set = ServerInfo.objects.get(id=server_id)
        update_set.salt_name = salt_name
        update_set.server_name = server_name
        update_set.cpu = cpu
        update_set.cpu_core = cpu_core
        update_set.system = system
        update_set.ip_addr = ip_addr
        update_set.ram = ram
        # update_set.add_date = add_date
        update_set.group_id = ServerGroup.objects.get(id=group_id)
        update_set.save()
        return redirect('/saltapi/server')

#删除服务器
def serverdelete(request,server_id):
    server = ServerInfo.objects.get(id=server_id)
    server.delete()
    return redirect('/saltapi/server')

#查询用户权限组
def userpriv(request):
    userpriv_set = UserPriv.objects.all()
    return render(request,'saltapi/userpriv.html',{'userpriv_set': userpriv_set})

#添加用户权限组
def userpriv_add(request):
    if request.method == 'GET' :
        return render(request,'saltapi/userpriv_add.html',)
    else:
        priname = request.POST.get('priv_name')
        pricomment = request.POST.get('comment')
        UserPriv.objects.create(priv_name=priname,comment=pricomment)
        return redirect('/saltapi/userpriv')

#删除用户权限组
def userpriv_del(request,priv_id):
    userpriv = UserPriv.objects.get(id=priv_id)
    userpriv.delete()
    return redirect('/saltapi/userpriv')

#修改用户权限组
def userpriv_change(request,priv_id):
    if request.method == 'GET':
        priv = UserPriv.objects.get(id=priv_id)
        return render(request,'saltapi/userpriv_change.html',{'priv': priv })
    else:
        privname= request.POST.get('priv_name')
        privcomm= request.POST.get('comment')
        priv = UserPriv.objects.get(id=priv_id)
        priv.priv_name = privname
        priv.comment = privcomm
        priv.save()
        return redirect('/saltapi/userpriv')

#查询用户信息
def user(request):
    try:
        user_set = UserInfo.objects.all()
    except UserInfo.DoesNotExist:
        render(request,'saltapi/user.html',{'user_set': user_set,})
    return render(request,'saltapi/user.html',{'user_set': user_set})


#删除用户
def user_del(request,user_id):
    user = UserInfo.objects.get(id= user_id)
    user.delete()
    return redirect('/saltapi/user')

#修改用户信息
def user_change(request,user_id):
    if request.method == 'GET':
        user = UserInfo.objects.get(id=user_id)
        userpriv = UserPriv.objects.all()
        return render(request,'saltapi/user_change.html',{'user': user,'userpriv': userpriv})
    else:

        username = request.POST.get('user_name')
        usercnname = request.POST.get('user_cnname')
        userpass = request.POST.get('user_pass')
        useremail = request.POST.get('user_email')
        userprivid = request.POST.get('user_priv_id')

        updateuser = UserInfo.objects.get(id=user_id)
        updateuser.user_name = username
        updateuser.user_cnname = usercnname
        updateuser.user_pass = userpass
        updateuser.user_email = useremail
        updateuser.user_priv_id = UserPriv.objects.get(id = userprivid)
        updateuser.save()
        return redirect('/saltapi/user')

def user_add(request):
    if request.method == 'POST':
        username = request.POST.get('user_name')
        usercnname = request.POST.get('user_cnname')
        userpass = request.POST.get('user_pass')
        useremail = request.POST.get('user_email')
        userprivid = UserPriv.objects.get(id=request.POST.get('user_priv_id'))
        UserInfo.objects.create(user_name=username,user_cnname=usercnname,user_pass=userpass,user_email=useremail,user_priv_id=userprivid)
        return redirect('/saltapi/user')
    else:
        userpriv = UserPriv.objects.all()
        return render(request,'saltapi/user_add.html',{'userpriv': userpriv})














