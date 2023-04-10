from django.urls import path, reverse_lazy, reverse
from django.contrib.auth import views as auth_views
from . import views


app_name = 'app'

urlpatterns = [
    path('', views.root, name='root'),
    # 회원가입 페이지
    path('sign-up', views.sign_up, name='sign_up'),
    path('login', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='app/main_page.html'), name='logout'),
    path('create', views.create_cloth, name='create'),
]
