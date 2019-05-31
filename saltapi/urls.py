from django.urls import path
from . import views

app_name = 'saltapi'
urlpatterns =[
    path('',views.index,name='index'),
    path('saltapicmd/',views.saltapicmd,name='saltapicmd'),

]

