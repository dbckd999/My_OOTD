from django import forms
from .models import UserClothes, SevUser
from django.contrib.auth.forms import UserCreationForm


class UserClothesForm(forms.ModelForm):
    class Meta:
        model = UserClothes
        fields = ['user_id', 'username', 'cloth_name', 'cloth_var', 'cloth_col_1', 'cloth_col_2']


# 회원가입 폼
class SevUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = SevUser
        fields = (
            'username'
            , 'password1'
            , 'password2'
            , 'email'
            , 'nickname'
            , 'is_male'
            , 'phone'
            , 'skin_color'
        )
