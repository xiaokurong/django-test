from django.urls import path
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
    path('other',views.other,name='other'),
    path('insert',views.insert,name='insert'),
    path('refresh',views.refresh,name='refresh'),

]

