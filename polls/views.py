from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from django.template import loader
from django.http import Http404

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template= loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context,request))
# Create your views here.

def detail(request,question_id):
    try:
        question=Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question does not exist')
    return render(request,'polls/details.html',{'question': question,})

def results(request,question_id):
    response='you are looking at the results of question %s.'
    return HttpResponse(response % question_id)

def vote(request,question_id):
    return HttpResponse('you are voting on question %s. ' % question_id)

