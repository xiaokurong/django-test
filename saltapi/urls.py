from django.urls import path,re_path
from . import views

app_name = 'saltapi'
urlpatterns =[
    path('',views.brief,name='brief'),
    path('saltapicmd', views.saltapicmd, name='saltapicmd'),
    path('history',views.history,name='history'),
    # path('runcmd',views.runcmd,name='runcmd'),

    path('servergroup',views.servergroup,name='servergroup'),
    path('servergroup_change/<int:group_id>',views.servergroup_change,name='servergroup_change'),
    path('servergroup_add',views.servergroup_add,name='servergroup_add'),
    path('servergroup_del/<int:group_id>',views.servergroup_del,name='servergroup_del'),
    path('user',views.user,name='user'),
    path('user_del/<int:user_id>',views.user_del,name='user_del'),
    path('user_change/<int:user_id>',views.user_change,name='user_change'),
    path('user_add',views.user_add,name='user_add'),
    path('other',views.other,name='other'),
    path('server',views.server,name='server'),
    path('serveradd',views.serveradd,name='serveradd'),
    path('refresh',views.refresh,name='refresh'),
    # re_path(r'serverchange/(\d+)/',views.serverchange,name='serverchange'),
    path('serverchange/<int:server_id>',views.serverchange,name='serverchange'),
    path('serverdelete/<int:server_id>',views.serverdelete,name='serverdelete'),
    path('userpriv',views.userpriv,name='userpriv'),
    path('userpriv_add',views.userpriv_add,name='userpriv_add'),
    path('userpriv_del/<int:priv_id>',views.userpriv_del,name='userpriv_del'),
    path('userpriv_change/<int:priv_id>',views.userpriv_change,name='userpriv_change'),
    path('test',views.test,name='test'),
    path('test1',views.test1,name='test1'),
    path('servergroupapi',views.servergroupapi,name='servergroupapi'),
    path('historyapi',views.historyapi,name='historyapi'),
    path('serverapi',views.serverapi,name='serverapi'),
    # path('testdata',views.testdata,name='testdata'),

]

