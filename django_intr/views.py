# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse


def hello_world(request):
    return HttpResponse("Hell world")

def hello(request):
    context = {}
    context['hello'] = 'Hello,world!'
    return render(request,'hello.html',context)

def index(request):
    return HttpResponse("this is index page!")