from django import forms
from .models import UserClothes

class UserClothesForm(forms.ModelForm):
    class Meta:
        model = UserClothes
        fields = ['user_id', 'username', 'cloth_name', 'cloth_var', 'cloth_col_1', 'cloth_col_2', 'cloth_img']