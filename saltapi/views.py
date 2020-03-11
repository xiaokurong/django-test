from django.shortcuts import render, redirect
# from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from . import saltapi
from .models import ServerInfo,UserInfo,UserPriv,ServerGroup, OffenCommand
from collections import defaultdict
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http.response import JsonResponse
import json
from django.db.models import Count
from django.db import connection
from django.core import serializers


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
        groupname = request.POST.get('group_name')
        if len(hostnames) == 0 and len(groupname)==0 :
            error="未输入主机名或服务器组名"
            return render(request,'saltapi/saltapirun.html',{'login_err': error})
        elif len(hostnames) == 0 and len(groupname) >0:
            salt_client = groupname
            print(salt_client)
        elif len(hostnames) > 0 and len(groupname) ==0:
            salt_client = hostnames
        else:
            salt_client = hostnames+','+groupname





        try:
            sapi=saltapi.SaltAPI(url='https://172.20.20.70:8000/',username='saltapi',password='saltapi')
            # salt_client=hostnames+','+groupname
            salt_method='cmd.run'
            salt_params = commands
            reinfos = sapi.salt_command(salt_client,salt_method,salt_params)
            OffenCommand.objects.create(command_name=commands, hostnames=hostnames,command_result=reinfos)
            group_set = ServerGroup.objects.all()
            return render(request,'saltapi/saltapirun.html',{'login_err': reinfos,'group_set':group_set})
        except Exception as error:
            return render(request,'saltapi/saltapirun.html',{'login_err': error})

    else:
        group_set = ServerGroup.objects.all()

        return render(request,'saltapi/saltapirun.html',{'group_set':group_set})

#查询历史命令
def history(request):
    #分页显示
    history_set = OffenCommand.objects.all()
    #每页三行
    page_histroy_set =  Paginator(history_set,3)
    page = request.GET.get('page')
    try:
        page_histroy = page_histroy_set.page(page)
    except PageNotAnInteger:
        page_histroy = page_histroy_set.page(1)
    except EmptyPage:
        page_histroy = page_histroy_set.page(page_histroy_set.num_pages)

    return render(request,'saltapi/history.html',{'page_history': page_histroy})

    #无分页显示
    # try:
    #     history_set = OffenCommand.objects.all()
    #     return render(request, 'saltapi/history.html', {"history_set": history_set})
    # except Exception as error:
    #     return  render(request,'saltapi/history.html',{"error": error})

#查询历史命令接口
def historyapi(request):
    history_set = OffenCommand.objects.values('command_name').annotate(c=Count('command_name')).values('command_name',"c").order_by('-c')[:5]
    history = {}
    history['data']=list(history_set)
    return JsonResponse(history)




#查询服务器分组信息
def servergroup(request):
    try:
        server_group_set = ServerGroup.objects.all()
        server_set = ServerInfo.objects.all()
        return render(request, 'saltapi/servergroup.html', {'server_group_set': server_group_set, 'server_set': server_set})
    except Exception as error:
        return render(request,'saltapi/servergroup.html',{'error': error})

#查询服务器分组接口
def servergroupapi(request):
    data={}
    try:
        server_group_set = ServerGroup.objects.annotate(c=Count('serverinfo__id')).values('group_name','c')
        # data['list']=json.loads(serializers.serialize('json',server_group_set))
        # return JsonResponse(data)
        data['list']=list(server_group_set)
        return JsonResponse(data)
    except Exception as error:
        return HttpResponse(json.dumps(error), content_type='application/json')
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

#查询服务器信息
def server(request):

    try:
        server_set = ServerInfo.objects.all()
        group_set = ServerGroup.objects.all()
        return render(request,'saltapi/server.html',{'server_set': server_set,'group_set': group_set})

    except ServerInfo.DoesNotExist:
        return  render(request,'saltapi/server.html',{'server_set': server_set, })

#查询服务器信息接口
def serverapi(request):
    cursor = connection.cursor()
    cursor.execute("select (SELECT SUM(bb.count) from (select DATE_FORMAT(add_date,'%Y%m%d') days, count(*) count from saltapi_serverinfo   group by  days ) bb WHERE aa.days >=bb.days ) totalcount,aa.count daycount, aa.days    from (select DATE_FORMAT(add_date,'%Y%m%d') days, count(*) count from saltapi_serverinfo   group by  days  ) aa  ")
    rows= cursor.fetchall()
    newrow=[]
    jsonrow={}
    for i in rows:
        newrow.append(i)
    jsonrow['data']=newrow
    return JsonResponse(jsonrow)


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
    if request.method == 'GET':
    #     # return render(request, 'saltapi/refresh.html')
    #


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
    else:

        salt_name = request.POST['salt_name']
        server_name = request.POST['server_name']
        cpu = request.POST['cpu']
        cpu_core = request.POST['cpu_core']
        system = request.POST['system']
        ip_addr = request.POST['ip_addr']
        ram = request.POST['ram']
        disk = request.POST['disk']

        ServerInfo.objects.create(salt_name=salt_name, server_name=server_name, cpu=cpu, cpu_core=cpu_core,system=system, ip_addr=ip_addr, ram=ram, disk=disk)


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

def test(request):
    # data={
    #     'name': 'vitor',
    #     'location': 'finland',
    #     'is_active': True,
    #     'count': 28
    # }
    # return JsonResponse(data)
    # name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
    name_dict = {
    "data_pie" : [
    {"value":235, "name":"视频广告"},
    {"value":274, "name":"联盟广告"},
    {"value":310, "name":"邮件营销"},
    {"value":335, "name":"直接访问"},
    {"value":400, "name":"搜索引擎"}
    ]
}
    return HttpResponse(json.dumps(name_dict), content_type='application/json')

def test1(request):
    return render(request,'saltapi/test1.html')

def testdata(request):
    for i in range(20):
        salt_name = 'test'+str(i)
        server_name = 'test'+str(i)
        cpu = 'i5'
        cpu_core = 4
        system = 'CentOS6'
        ip_addr= '172.20.20.21'
        ram = '400'
        disk = '200'
        ServerInfo.objects.create(salt_name=salt_name, server_name=server_name, cpu=cpu, cpu_core=cpu_core,system=system, ip_addr=ip_addr, ram=ram, disk=disk)
    return HttpResponse('添加成功！')















