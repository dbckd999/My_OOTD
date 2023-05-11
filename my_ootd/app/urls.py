from django.urls import path, reverse_lazy, reverse
from django.contrib.auth import views as auth_views
from . import views


app_name = 'app'

urlpatterns = [
    path('', views.root, name='root'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('login', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='app/main.html'), name='logout'),
    path('mycloset', views.post_cloth, name='mycloset'),
    path('update_cloth', views.update_cloth, name='update_cloth'),
    path('create_user', views.create_user, name='create_user'),
    path('color_match_test', views.get_close_color, name='color_match_test'),

    # ajax
    path('retry_recommend_cody', views.retry_recommend_cody, name='retry_recommend_cody'),
    path('save_my_style', views.save_my_style, name='save_my_style'),
]
