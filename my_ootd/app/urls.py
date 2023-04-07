from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('welcome/', views.welcome, name='welcome'),
    path('', views.create_cloth_db, name='create_cloth_db')
]
