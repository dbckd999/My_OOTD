from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.models import User
from django.urls import reverse

from .models import UserClothes
from .forms import UserClothesForm


# 다른페이지 이동 편의로 만듦
def root(request):
    context = {
        "user": request.user,
    }
    return render(request, 'app/idx.html', context)


# 회원가입
# https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in
def sign_up(request):
    if request.method == 'POST':
        user = User(
            # , nickname=request.POST['nickname'] # Django 기본제공 User 커스텀 필요
            username=request.POST['username'], password=request.POST[
                'password'], email=request.POST['email'], last_name=request.POST['nickname']
        ).save()
        return redirect('/app/')

    return render(request, 'app/signup.html')


# 로그아웃
# https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-out
def logout(request):
    logout(request)


# 옷 db에 저장, 조회, 삭제
def create_cloth(request):
    if request.method == 'POST':
        # db 전체 삭제
        # UserClothes.objects.all().delete()
        post = UserClothes()
        user = User()
        # "index.html" 색상 제외 input text 칸 3개
        # 맨 왼쪽에 userID 입력 시 userID와 관련된 내용 모두 삭제
        # 맨 왼쪽 제외 나머지 두 칸은 각각 옷이름, 옷종류
        if user.is_authenticated:
            user_id_delete = request.POST["userID_Delete"]
            post.userID = request.user.id
            post.username = request.user.get_full_name()
            post.cloth_name = request.POST['cloth_name']
            post.cloth_var = request.POST['cloth_var']
            post.cloth_col_1 = request.POST['cloth_col_1']
            post.cloth_col_2 = request.POST['cloth_col_2']

            if user_id_delete != "":
                delete_id = UserClothes.objects.filter(userID=user_id_delete)
                delete_id.delete()
            elif post.cloth_name != "" and post.cloth_var != "":
                post.save()
        return redirect('/app/create')

    else:
        userClothes_post = {}
        # db 모든 데이터 조회
        # userClothes_post["queryset"] = UserClothes.objects.all()

        # '''여기에 userID 입력''' 에 userID 입력 시 userID와 관련된 모든 데이터 조회
        # 조회 시 나오는 내용 : 유저 고유 번호, 별명, 옷 이름, 옷 종류, 색1, 색2
        userClothes_post["queryset"] = UserClothes.objects.filter(
            userID='''여기에 userID 입력''')
        return render(request, 'app/clothes.html', userClothes_post)


def main_page(request):
    return render(request, 'app/main_page.html')
