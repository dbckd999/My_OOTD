from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.models import User
from django.urls import reverse

from .models import UserClothes
from .forms import UserClothesForm


# 다른페이지 이동 편의로 만듦
def root(request):
    return render(request, 'app/idx.html')


def welcome(request):
    template = loader.get_template('app/welcome.html')
    return render(request, 'app/welcome.html')


# 회원가입
# https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in
def sign_up(request):
    if request.method == 'POST':
        user = User(
            username=request.POST['username']
            , password=request.POST['password']
            # , nickname=request.POST['nickname'] # Django 기본제공 User 커스텀 필요
            , email=request.POST['email']
            , last_name=request.POST['nickname']
        ).save()
        return redirect('/app/')

    return render(request, 'app/signup.html')


# 로그아웃
# https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-out
def logout(request):
    logout(request)
