"""django_intr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import  views,testdb
from django.conf.urls import url
# from testmodel import views as test_views
# import sys
# sys.path.append('G:\\python_source\\django_test\\django_intr')




urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/',views.hello),
    url(r'^$',views.index),
    url(r'^testdb$',testdb.testdb),
    path('blog/',include('blog.urls',namespace='blog')),
    url(r'search_form',views.search_form),
    url(r'search$',views.search),
    url(r'search_post$',views.search_post),
]
