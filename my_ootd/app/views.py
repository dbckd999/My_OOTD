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

def create_cloth_db(request):
    if (request.method == 'POST'):
        userclothes = UserClothes()

        # UserCLothes 클래스에 각 입력 내용 db에 저장
        userclothes.tmp_userid = request.POST('userID')
        userclothes.cloth_name = request.POST('cloth_name')
        userclothes.cloth_var = request.POST('cloth_var')
        userclothes.cloth_col_1 = request.POST('cloth_col_1')
        userclothes.cloth_col_2 = request.POST('cloth_col_2')
        

        # 테스트 UI
        # 맨 왼쪽부터 userID, 옷 이름, 옷 종류, 색1, 색2
        # 맨 왼쪽 칸을 비우고 나머지 작성 후 버튼 누르면 db 저장
        # 맨 왼쪽 칸에 userID 입력하면 userID와 관련 된 내용 모두 삭제
        # 맨 왼쪽 칸이 입력이 되면 삭제만 가능 / 저장은 불가능
        if (id != ""):
            delete_id = UserClothes.objects.filter(userID = userclothes.tmp_userid)
            delete_id.delete()
        elif (userclothes.cloth_name != "" and userclothes.cloth_var != ""):
            userclothes.save()

        return redirect('create_cloth_db')
    
    # 아래 '''여기에 userID 입력''' 에 userID 입력 시 userID와 관련된 내용 모두 조회    
    else:
        userClothes_post = {}
        userClothes_post["queryset"] = UserClothes.objects.filter(cloth_name='''여기에 userID 입력''')
        return render(request, 'index.html', {'cloth_data':userClothes_post})         

