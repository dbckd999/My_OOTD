from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
# Create your views here.


def index(request):
    return HttpResponse("Hello world")


def welcome(request):
    template = loader.get_template('app/welcome.html')
    context = {}
    return render(request, 'app/welcome.html')
