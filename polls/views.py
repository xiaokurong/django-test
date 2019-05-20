from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('hello,world,this is my poll index!')
# Create your views here.
