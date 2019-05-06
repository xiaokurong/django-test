# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators import csrf

def hello_world(request):
    return HttpResponse("Hell world")

def hello(request):
    context = {}
    context['hello'] = 'Hello,world!'
    return render(request,'hello.html',context)

def index(request):
    return HttpResponse("this is index page!")

def search_form(request):
    return render_to_response('templates/search_form.html')

def search(request):
    request.encoding='utf-8'
    if 'q' in request.GET:
        message = '你搜索的内容为: ' + request.GET['q']
    else:
        message = '你提交了空表单！'
    return HttpResponse(message)

def search_post(request):
    ctx ={}
    request.encoding='utf-8'
    if request.POST:
        ctx['rlt'] = request.POST['q']

    return render(request,'templates/post.html',ctx)