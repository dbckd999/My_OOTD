from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.db import IntegrityError

from .models import UserClothes, SevUser, CodyLog
from .forms import UserClothesForm, SevUserCreationForm
from .personal_colors import PersonalColor

from .weather import weather, select_weather_icon_name

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import random
import json
import math

p_color = {}

def root(request):
    # if ['weather', 'weather_icon_filename'] not in request.session:
     
    res = weather()
    request.session['weather'] = res
    request.session['weather_icon_filename'] = select_weather_icon_name(res['SKY_st'], res['PTY_st'])

    try:
        context = {        
            # "_userdata": UserClothes.all_user_datas(UserClothes(), SevUser.objects.get(id=request.user.id)),
            "userdata": UserClothes.objects.filter(user_id=request.user.id, cloth_var='top'),
            "cody": cloth_all_recommend(request),
            "saved_cody": saved_cody(request),
            "category": ('top', 'pants', 'outer', 'shoes', 'accessory')  # 카테고리 조회 전용
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
    return render(request, 'app/create_user.html', context)


# 로그아웃
# https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-out
def logout(request):
    logout(request)


# 옷 db에 저장, 조회, 삭제
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
                usercloth = UserClothes.objects.get(id=delete_cloth)

                usercloth.delete_cloth()
                #usercloth.delete()
            elif 'update_cloth' in request.POST:
                update_cloth = request.POST['update_cloth']

                userClothes_update = UserClothes.objects.get(id=update_cloth)                
                return render(request, 'app/cloth_update.html', {'update': userClothes_update})
            elif 'create_cloth' in request.POST:           
                post.user_id = SevUser.objects.get(id=request.user.id)
                post.username = user.get_full_name()
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
        return render(request, 'app/clothes.html', userClothes_post)

# 옷 정보 업데이트
def update_cloth(request):
    if request.method == 'POST':
        user = SevUser()
    # 수정 버튼을 통해 옷 정보 수정
        if 'updateConfirm' in request.POST:
            cloth_id = request.POST['updateConfirm']
            cloth_update = UserClothes.objects.get(id=cloth_id)
            cloth_img_tmp = cloth_update.cloth_img
            
            cloth_update.user_id = SevUser.objects.get(id=request.user.id)
            cloth_update.username = user.get_full_name()          
            cloth_update.cloth_name = request.POST['update_cloth_name']
            cloth_update.cloth_var = request.POST['update_cloth_var']
            cloth_update.cloth_col_1 = request.POST['update_cloth_col_1']
            cloth_update.cloth_col_2 = request.POST['update_cloth_col_2']
            if (request.FILES.get('update_cloth_img')):
                cloth_update.delete_old_cloth()
                cloth_update.cloth_img = request.FILES.get('update_cloth_img')
            else:
                cloth_update.cloth_img = None

            if cloth_update.cloth_name != "" and cloth_update.cloth_var != "":
                if cloth_update.cloth_img == None:
                    # 사진을 바꾸지 않으면 이전 사진 파일 그대로 사용
                    cloth_update.cloth_img = cloth_img_tmp
                    cloth_update.save()

                else:
                    cloth_update.save()
        previouspage = request.POST.get('previouspage', '/')
        return redirect(previouspage)
    
def get_close_color(request):
    if request.method == 'POST':

        retrieve = SevUser.objects.get(id=request.user.id)

        r = request.POST['R']
        g = request.POST['G']
        b = request.POST['B']
        c_var = request.POST['col_cloth_var']
        p_col_var = request.POST['p_col_var']

        cloth = UserClothes.all_user_datas(UserClothes(), retrieve)
        cloth_col = []
        count = 0

        for i in cloth:
            data_tmp = []
            tmp = i['cloth_col_1']
            nm = i['cloth_name']
            col_cloth_var = i['cloth_var']
            if (c_var == col_cloth_var):
                count += 1
            for i in (1, 3, 5):
                decimal = int(tmp[i:i+2], 16)
                data_tmp.append(decimal)

            cloth_col.append((nm, tuple(data_tmp), col_cloth_var))
        
        
        p_col = PersonalColor.get_personal_color(PersonalColor(), int(p_col_var) - 1)
        MYCOL = p_col
        dist = []
        mycol = []
        for c in MYCOL:
            for i in (1, 3, 5):
                decimal = int(c[i:i+2], 16)
                mycol.append(decimal)
                
            for i in range(len(cloth_col)):
                name = cloth_col[i][0]
                t_col = cloth_col[i][1]
                t_var = cloth_col[i][2]
                if (t_var != c_var):
                    continue                
                t_r, t_g, t_b = t_col                
                distance = math.sqrt((mycol[0] - t_r)**2 + (mycol[1] - t_g)**2 + (mycol[2] - t_b)**2)
                dist.append((distance, t_col, name, t_var, c))            
            
            mycol.clear()
        
        dist.sort()        
        tmp = []
        for i in range(len(dist)):        
            if (dist[i][2] not in tmp):
                print((i+1), ": 옷 이름: ", dist[i][2],  "  색: ", dist[i][1], "  거리: ", round(dist[i][0], 2), " 종류 : ", dist[i][3], " 비교한 색: ", dist[i][4])            
                tmp.append(dist[i][2])
            else:
                continue
        color_match = { 
            "user": request.user,
            "userdata": UserClothes.all_user_datas(UserClothes(), retrieve),
            "colormatch" : dist
            }

        return render(request, 'app/color_match_test.html', color_match)

    else:
        retrieve = SevUser.objects.get(id=request.user.id)
        userClothes_post = {
            "user": request.user,
            "userdata": UserClothes.all_user_datas(UserClothes(), retrieve),
        }
        # 조회 시 나오는 내용 : 별명, 옷 이름, 옷 종류, 색1, 색2
        return render(request, 'app/color_match_test.html', userClothes_post)

def select_color_test(request):
    p_cols = ["BSp", "LSp", "TSp", "SSu", "LSu", "TSu", "DAu", "SAu", "TAu", "DWi", "TWi", "BWi"]
    isFirst = True

    f_col, s_col, t_col = 0, 0, 0
    
    if (not isFirst):
        while (s_col == f_col):
            f_col = random.randrange(0, 12)
            s_col = random.randrange(0, 12)
    else:
        while (s_col == f_col or s_col == t_col or f_col == t_col):
            f_col = random.randrange(0, 12)
            s_col = random.randrange(0, 12)
            t_col = random.randrange(0, 12)
    
    print("F:", f_col, "S:", s_col, "T:", t_col)

    col = {
        "f": p_cols[f_col],
        "s": p_cols[s_col],
        "t": p_cols[t_col]
    }

    return render(request, 'app/select_color_test.html', col)
        


def create_user(request):
    return render(request, 'app/create_user.html')


# 다시 추천하기 버튼 누를 때 호출
@csrf_exempt
def retry_recommend_cody(request):
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
    cloth_len = len(UserClothes.objects.filter(user_id=request.user.id, cloth_var=cloth_type))
    if cloth_len != 0:
        color_pick = random.randrange(0, cloth_len)
        # print(color_pick)
        cloth = UserClothes.objects.filter(user_id=request.user.id, cloth_var=cloth_type)[color_pick]
        return cloth
    else:
        return None


# 코디 추천 결과 이미지 이름배열 반환
def cloth_all_recommend(request) -> dict:
    cody = dict()
    ids = list()
    category = ('top', 'pants', 'outer', 'shoes', 'accessory')

    for c in category:
        cloth = cloth_recommend(c, request)
        if cloth is not None:
            cody[c] = str(cloth.cloth_img)
            ids.append(cloth.id)
        if cloth is None:
            ids.append(None)
    request.session['cody_id'] = ids
    return cody


# 추천 결과 저장
@csrf_exempt
def save_my_style(request):
    cody = request.session['cody_id']
    print(cody)
    c = CodyLog()
    c.user_id = request.user
    c.top = UserClothes.objects.get(id=cody[0]) if cody[0] is not None else None
    c.pants = UserClothes.objects.get(id=cody[1]) if cody[1] is not None else None
    c.outer = UserClothes.objects.get(id=cody[2]) if cody[2] is not None else None
    c.shoes = UserClothes.objects.get(id=cody[3]) if cody[3] is not None else None
    c.accessory = UserClothes.objects.get(id=cody[4]) if cody[4] is not None else None

    try:
        c.save()
        return HttpResponse('Saved', status=200)
    except IntegrityError as e:
        return HttpResponse(e, status=409)


def saved_cody(request):
    c = CodyLog.objects.filter(user_id=request.user.id)
    saved = list()
    for cc in c:
        saved.append([
            str(cc.top.cloth_img),
            str(cc.pants.cloth_img),
            str(cc.outer.cloth_img),
            str(cc.shoes.cloth_img),
            str(cc.accessory.cloth_img)
        ])

    return saved


def my(request):
    return render(request, 'app/user/userinfo.html', {})


def personal_color(request):
    if request.method == 'GET':
        print(request.GET.get('picked_color'))
    return render(request, 'app/color.html', {})


# 카테고리 별 옷장 조회
@csrf_exempt
def clothes_category(request):
    if request.method == 'POST':
        key = request.POST.get('category')

        c = UserClothes.objects.filter(user_id=request.user.id, cloth_var=key)
        c_list = []
        for i in c:
            c_list.append(str(i.cloth_img))

        try:
            return HttpResponse(str(c_list), status=200)
        except IntegrityError as e:
            return HttpResponse(str(e), status=409)

    return HttpResponse(status=400)  # 유효하지 않은 요청인 경우 400 응답 반환
