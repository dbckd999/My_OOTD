from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .models import UserClothes
from .forms import UserClothesForm
# Create your views here.


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
            username=request.POST['id']
            , password=request.POST['password']
            # , nickname=request.POST['nickname'] # Django 기본제공 User 커스텀 필요
            , email=request.POST['email']
            , last_name=request.POST['nickname']
        ).save()
        print(user)

    return render(request, 'app/idx.html')


# 로그인
# def sign_in(request):
#     pass
    # logger.debug('asdf')
    # print('sign-in..asdfasdf.')
    # if request.method == 'POST':
    #     print('sign-in...')
    #     username = request.POST["username"]
    #     password = request.POST["password"]
    #     # 사용자 인증
    #     user = authenticate(request, username=username, password=password)
    #     print(user)
    #     if user is not None:
    #         print('login suc')
    #         login(request, user)
    #         return redirect('app/root')
    #     else:
    #         print('login fail')
    #         return render(request, 'app/sign-in.html')
    #
    # elif request.method == 'GET':
    #     return render(request, 'app/sign-in.html')


# 로그아웃
# https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-out
def logout(request):
    logout(request)
