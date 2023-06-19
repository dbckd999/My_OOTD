import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField
import re


# SevUser 객체 생성 시 '-'없는 휴대전화 번호 검증
def validate_phone_number(phone):
    pattern = re.compile(r"^01[0-1]\d{8}$")
    if not pattern.match(phone):
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': phone},
        )


# 서비스에 맞게 적용한 유저 클래스
class SevUser(User):
    nickname = models.CharField('nickname', null=False, max_length=20, default='init_nick')
    is_male = models.BooleanField('isMale', null=False)
    phone = models.CharField('phone', max_length=11, validators=[validate_phone_number])
    skin_color = ColorField(default='#FFFFFF')  # 피부색

# 사용자의 옷 데이터를 관리합니다.
# 사용자 고유번호는 장고에 기본 제공되는 id 속성을 사용합니다.
# 계정을 참고해서 CRD


class UserClothes(models.Model):
    # tmp_userid = models.CharField(max_length=10) # 임시 계정

    user_id = models.ForeignKey(SevUser, on_delete=models.CASCADE)  # 유저 고유 번호
    username = models.CharField(max_length=50, null=True)  # 유저이름
    cloth_name = models.CharField(max_length=50)  # 옷 이름
    cloth_var = models.CharField(max_length=30)  # 옷 종류 (자켓, 셔츠 등)
    cloth_col_1 = models.CharField(max_length=30)  # 옷 색깔 1
    cloth_col_2 = models.CharField(max_length=30)  # 옷 색깔 2

    def upload_cloth_img(instance, filename):
        upload_to = ""
        uuid_name = uuid4().hex
        extension = os.path.splitext(filename)[-1].lower()

        return ''.join([upload_to, uuid_name + extension])
    
    cloth_img = models.ImageField(null=True, upload_to=upload_cloth_img, blank=True) # 옷 사진

    def delete_cloth(self, *args, **kargs):
        if self.cloth_img:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.cloth_img.path))
        super(UserClothes, self).delete(*args, **kargs)

    def delete_old_cloth(self):
        if self.cloth_img:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.cloth_img.path))

    def __str__(self):
        return f'{self.user_id} {self.username} {self.cloth_name} {self.cloth_var} {self.cloth_col_1} {self.cloth_col_2}'
    
    def all_user_datas(self, id):
        datas = []

        for data in UserClothes.objects.filter(user_id=id):
            datas.append({
                'id': data.id,
                'userID': str(data.user_id),
                'username': str(data.username),
                'cloth_name': str(data.cloth_name),
                'cloth_var': str(data.cloth_var),
                'cloth_col_1': str(data.cloth_col_1),
                'cloth_col_2': str(data.cloth_col_2),
                'cloth_img': data.cloth_img
            })
        
        return datas


class CodyLog(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='_user_id')
    top = models.ForeignKey(UserClothes, on_delete=models.CASCADE, related_name='_top', null=True)
    pants = models.ForeignKey(UserClothes, on_delete=models.CASCADE, related_name='_pants', null=True)
    outer = models.ForeignKey(UserClothes, on_delete=models.CASCADE, related_name='_outer', null=True)
    shoes = models.ForeignKey(UserClothes, on_delete=models.CASCADE, related_name='_shoes', null=True)
    accessory = models.ForeignKey(UserClothes, on_delete=models.CASCADE, related_name='_accessory', null=True)

    # 중복방지
    class Meta:
        unique_together = [["top", "pants", "outer", "shoes", "accessory"]]

    def __str__(self):
        try:
            return f'{self.user_id}:[{self.top.id}, {self.pants.id}, {self.outer.id}, {self.outer.id}' \
               f', {self.shoes.id}, {self.accessory.id}]'
        except AttributeError:
            return "Err"
