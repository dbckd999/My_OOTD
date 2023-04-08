from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    # path('', views.welcome, name='welcome'),
    path('', views.root, name='root'),
    # 회원가입 페이지
    path('sign-up', views.sign_up, name='sign_up'),
    # 회원가입 데이터 전송
    path('sign_up_proc', views.sign_up_proc, name='sign_up_proc'),
    path('login', views.get_login_page, name='login'),
]
