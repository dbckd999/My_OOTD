from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('welcome/', views.welcome, name='welcome'),
    path('welcome/sign-up', views.sign_up, name='sign_up'),
    path('welcome/sign-up-proc', views.sign_up_proc, name='sign_up_proc'),
]
