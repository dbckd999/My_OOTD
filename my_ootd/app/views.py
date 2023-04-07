from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from .models import UserClothes
from .forms import UserClothesForm
# Create your views here.


def index(request):
    return HttpResponse("Hello world")


def welcome(request):
    template = loader.get_template('app/welcome.html')
    context = {}
    return render(request, 'app/welcome.html')


def sign_up(request):
    return render(request, 'app/signup.html')


# 가입할 데이터를 받습니다.
def sign_up_proc(request):
    if request.method == 'POST':
        # print(request.POST)
        user = User(_id=request.POST['id']
                    , password=request.POST['password']
                    , nickname=request.POST['nickname']
                    )
        print(user)
        user.create()
    return render(request, 'app/signup.html', None)
