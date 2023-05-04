from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .models import UserClothes, SevUser
from .forms import UserClothesForm, SevUserCreationForm

from .weather import weather, select_weather_icon_name

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
from django.http import HttpResponse
import random
import json


def root(request):
    # if ['weather', 'weather_icon_filename'] not in request.session:
     
    sevuser = SevUser()
    
    res = weather()
    request.session['weather'] = res
    request.session['weather_icon_filename'] = select_weather_icon_name(res['SKY_st'], res['PTY_st'])

    try:
        context = {        
            "userdata": UserClothes.all_user_datas(UserClothes(), SevUser.objects.get(id=request.user.id)),
        }
    except SevUser.DoesNotExist:
        context = {
        
        }       
        
    return render(request, 'app/main.html', context)


# 회원가입 https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in
# 폼 클래스 https://wikidocs.net/71303#formspy
def sign_up(request):
    if request.method == 'POST':
        form = SevUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
        return redirect('/')

    # 개발용 기본값
    context = {
        "form": SevUserCreationForm(initial={
            'username': 'my_test_id'
            # , 'password1': 'waenva3nwe'  # 입력 불가능
            # , 'password2': 'waenva3nwe'  # 입력 불가능
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


# 옷 db에 저장, 조회, 삭제, 업데이트
def post_cloth(request):
    if request.method == 'POST':
        # db 전체 삭제
        # UserClothes.objects.all().delete()

        post = UserClothes()        
        user = SevUser()        

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
                post.user_id = SevUser.objects.get(id=request.user.id)
                post.username = user.get_full_name() # 닉네임 안 나오는 버그 있음
                post.cloth_name = request.POST['cloth_name']
                post.cloth_var = request.POST['cloth_var']
                post.cloth_col_1 = request.POST['cloth_col_1']
                post.cloth_col_2 = request.POST['cloth_col_2']
                post.cloth_img = request.FILES.get('cloth_img')
            
                if post.cloth_name != "" and post.cloth_var != "" and post.cloth_img != None:
                    post.save()

        return redirect('/mycloset')
    else:
        retrieve = SevUser.objects.get(id=request.user.id)
        userClothes_post = {
            "user": request.user,
            "userdata": UserClothes.all_user_datas(UserClothes(), retrieve),
        }
        # 조회 시 나오는 내용 : 별명, 옷 이름, 옷 종류, 색1, 색2
        return render(request, 'app/clothes.html', userClothes_post)


def update_cloth(request):
    if request.method == 'POST':
        user = SevUser()
    # 수정 버튼을 통해 옷 정보 수정
        if 'updateConfirm' in request.POST:
            cloth_id = request.POST['updateConfirm']
            cloth_update = UserClothes.objects.get(id=cloth_id)   

            cloth_update.user_id = SevUser.objects.get(id=request.user.id)
            cloth_update.username = user.get_full_name()          
            cloth_update.cloth_name = request.POST['update_cloth_name']
            cloth_update.cloth_var = request.POST['update_cloth_var']
            cloth_update.cloth_col_1 = request.POST['update_cloth_col_1']
            cloth_update.cloth_col_2 = request.POST['update_cloth_col_2']
            cloth_update.cloth_img = request.FILES.get('update_cloth_img')
            
            if cloth_update.cloth_name != "" and cloth_update.cloth_var != "" and cloth_update.cloth_img != None:
                cloth_update.save()
        
        previouspage = request.POST.get('previouspage', '/')
        return redirect(previouspage)


def create_user(request):
    return render(request, 'app/create_user.html')


# ajax 테스트
@csrf_exempt
def test(request):
    if request.method == 'POST':
        res = json.dumps(cloth_all_recommend(request=request))
        return HttpResponse(res)


# 옷 하나 추천
def cloth_recommend(cloth_type: str, request) -> UserClothes or None:
    """
    :param request:
    :param cloth_type: 쿼리 시 사용할 옷의 종류(영어)
    :param weather: 날씨. 온도값
    1. 사용자의 퍼스널컬러 데이터 가져오기
    2. 퍼스널컬러 배열 중 하나 선택
    3. +날씨 고려해 긴팔/짧은팔 추천
    :return: 4. 색상값 중 가장 가까운 옷 선택
    """
    cloth_len = len(UserClothes.objects.filter(cloth_var=cloth_type))
    if cloth_len is not 0:
        color_pick = random.randrange(0, cloth_len)
        cloth = UserClothes.objects.filter(user_id=request.user.id, cloth_var=cloth_type)[color_pick]
        return cloth
    else:
        return None


# 코디 추천 결과 이미지 이름배열 반환
def cloth_all_recommend(request) -> dict:
    cody = dict()
    category = ('top', 'pants', 'outer', 'shoes', 'accessory')

    for c in category:
        cloth = cloth_recommend(c, request)
        if cloth is not None:
            cody[c] = str(cloth.cloth_img)

    return cody


# 추천 결과 저장
def save_my_style():
    pass
