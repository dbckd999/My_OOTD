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
        # "user": request.user,
    }
    return render(request, 'app/main_page.html', context)


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


# 옷 db에 저장, 조회, 삭제, 업데이트
def post_cloth(request):
    if request.method == 'POST':
        # db 전체 삭제
        # UserClothes.objects.all().delete()

        post = UserClothes()
        user = User()
        
        # "clothes.html" 색상 제외 input text 칸 2개
        # 두 칸은 각각 옷이름, 옷종류
        # 둘 중 하나라도 입력이 안 될 시 db에 저장 되지 않음
        if user.is_authenticated:

            # 삭제 버튼을 통해 지우고싶은 옷 삭제 가능
            # 수정 버튼을 통해 옷 정보 수정
            # 저장 버튼을 통해 옷 정보 저장
            if 'delete_cloth' in request.POST:
                delete_cloth = request.POST['delete_cloth']

                UserClothes.objects.filter(id=delete_cloth).delete()
            elif 'update_cloth' in request.POST:
                update_cloth = request.POST['update_cloth']

                userClothes_update = UserClothes.objects.get(id=update_cloth)                
                return render(request, 'app/cloth_update.html', {'update': userClothes_update})
            elif 'create_cloth' in request.POST:          
                post.user_id = User.objects.get(id=request.user.id)
                post.username = request.user.get_full_name()
                post.cloth_name = request.POST['cloth_name']
                post.cloth_var = request.POST['cloth_var']
                post.cloth_col_1 = request.POST['cloth_col_1']
                post.cloth_col_2 = request.POST['cloth_col_2']
                post.cloth_img = request.FILES['cloth_img']

                if post.cloth_name != "" and post.cloth_var != "":
                    post.save()

            # 수정 버튼을 통해 옷 정보 수정
            if 'updateConfirm' in request.POST:
                cloth_id = request.POST['updateConfirm']
                cloth_update = UserClothes.objects.get(id=cloth_id)
                
                cloth_update.user_id = User.objects.get(id=request.user.id)
                cloth_update.username = request.user.get_full_name()          
                cloth_update.cloth_name = request.POST['update_cloth_name']
                cloth_update.cloth_var = request.POST['update_cloth_var']
                cloth_update.cloth_col_1 = request.POST['update_cloth_col_1']
                cloth_update.cloth_col_2 = request.POST['update_cloth_col_2']
                cloth_update.cloth_img = request.FILES['update_cloth_img']

                if cloth_update.cloth_name != "" and cloth_update.cloth_var != "":
                    cloth_update.save()
            
        return redirect('/app/mycloset')
    else:
        retrieve = User.objects.get(id=request.user.id)
        userClothes_post = {
            "user": request.user,
            "userdata": UserClothes.all_user_datas(UserClothes(), retrieve)
        }
        # 조회 시 나오는 내용 : 별명, 옷 이름, 옷 종류, 색1, 색2
        return render(request, 'app/clothes.html', userClothes_post)


def login_page(request):
    return render(request, 'app/login_page.html')


def create_user(request):
    return render(request, 'app/create_user.html')
