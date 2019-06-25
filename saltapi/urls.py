from django.urls import path,re_path
from . import views

app_name = 'saltapi'
urlpatterns =[
    path('',views.brief,name='brief'),
    path('saltapicmd', views.saltapicmd, name='saltapicmd'),
    path('history',views.history,name='history'),
    # path('runcmd',views.runcmd,name='runcmd'),
    path('server',views.server,name='server'),
    path('servergroup',views.servergroup,name='servergroup'),
    path('user',views.user,name='user'),
    path('user_del/<int:user_id>',views.user_del,name='user_del'),
    path('user_change/<int:user_id>',views.user_change,name='user_change'),
    path('other',views.other,name='other'),
    path('insert',views.insert,name='insert'),
    path('refresh',views.refresh,name='refresh'),
    # re_path(r'serverchange/(\d+)/',views.serverchange,name='serverchange'),
    path('serverchange/<int:server_id>',views.serverchange,name='serverchange'),
    path('serverdelete/<int:server_id>',views.serverdelete,name='serverdelete'),
    path('userpriv',views.userpriv,name='userpriv'),
    path('userpriv_add',views.userpriv_add,name='userpriv_add'),
    path('userpriv_del/<int:userpriv_id>',views.userpriv_del,name='userpriv_del'),
    path('userpriv_change/<int:priv_id>',views.userpriv_change,name='userpriv_change'),

]

