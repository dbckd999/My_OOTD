from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .models import UserClothes, SevUser
from .forms import UserClothesForm, SevUserCreationForm


# 다른페이지 이동 편의로 만듦
def root(request):
    context = {
        # "user": request.user,
    }
    return render(request, 'app/main_page.html', context)


# 회원가입 https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in
# 폼 클래스 사용 https://wikidocs.net/71303#formspy
def sign_up(request):
    if request.method == 'POST':
        form = SevUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
        return redirect('/app/')

    context = {
        "form": SevUserCreationForm(initial={
            'username': 'my_test_id'
            , 'password1': 'waenva3nwe'
            , 'password2': 'waenva3nwe'
            , 'nickname': 'my_test_nick'
            , 'email': 'test@nav.com'
            , 'phone': '01044445555'
        })
    }
    return render(request, 'app/signup.html', context)


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

        # "clothes.html" 색상 제외 input text 칸 2개
        # 두 칸은 각각 옷이름, 옷종류
        # 둘 중 하나라도 입력이 안 될 시 db에 저장 되지 않음
        if user.is_authenticated:
            
            # 삭제 버튼을 통해 지우고싶은 옷 삭제 가능
            if 'delete_cloth' in request.POST:
                delete_cloth = request.POST['delete_cloth']
                UserClothes.objects.filter(id=delete_cloth).delete()

            post.user_id = User.objects.get(id=request.user.id)
            post.username = request.user.get_full_name()
            post.cloth_name = request.POST['cloth_name']
            post.cloth_var = request.POST['cloth_var']
            post.cloth_col_1 = request.POST['cloth_col_1']
            post.cloth_col_2 = request.POST['cloth_col_2']

            if post.cloth_name != "" and post.cloth_var != "":
                post.save()
        
        return redirect('/app/create')
    else:
        retrieve = User.objects.get(id=request.user.id)
        userClothes_post = {
            "user": request.user,
            "userdata": UserClothes.all_user_datas(UserClothes(), retrieve)
        }

        # 조회 시 나오는 내용 : 별명, 옷 이름, 옷 종류, 색1, 색2
        return render(request, 'app/clothes.html', userClothes_post)