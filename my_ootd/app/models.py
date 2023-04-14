import os
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


'''
# 예외처리
#           |내용|                                                                            |기대 결과|
    # 모든 칸에 특수 문자 입력               -- alert 창이 뜨고 해당 특수문자 삭제
    # 모든 칸 비움                          -- db에 데이터가 저장되지 않음 / 아무런 일도 일어나지 않음
    # 모든 칸 입력                          -- db에 입력한 데이터 저장
    # 모든 칸 중 한 칸 이상을 빼고 입력       -- db에 데이터가 저장되지 않음
    # 옷 사진 파일을 올리지 않음               -- db에 데이터가 저장되지 않음 / 아무런 일도 일어나지 않음
    # 삭제 버튼 클릭                         -- 삭제하려고 하는 옷만 삭제 됨
    # 수정 버튼 클릭                          -- 옷 정보 수정 페이지로 이동
    # 수정 사항 입력 후 수정 버튼 클릭         -- 옷 정보가 내가 의도한대로 수정 됨
    # 수정 페이지에서 사진을 업로드 하지 않음   -- 파일 선택 알림이 뜸
''' 


class UserClothes(models.Model):
    # tmp_userid = models.CharField(max_length=10) # 임시 계정

    user_id = models.ForeignKey(User, on_delete=models.CASCADE) # 유저 고유 번호
    username = models.CharField(max_length=50, null=True) # 유저이름
    cloth_name = models.CharField(max_length=50) # 옷 이름
    cloth_var = models.CharField(max_length=30) # 옷 종류 (자켓, 셔츠 등)
    cloth_col_1 = models.CharField(max_length=30) # 옷 색깔 1
    cloth_col_2 = models.CharField(max_length=30) # 옷 색깔 2

    def upload_cloth_img(instance, filename):
            upload_to = ""
            uuid_name = uuid4().hex
            extension = os.path.splitext(filename)[-1].lower()

            return ''.join([upload_to, uuid_name + extension])
    
    cloth_img = models.ImageField(null=True, upload_to=upload_cloth_img, blank=True) # 옷 사진

    def __str__(self):
        return f'{self.user_id} {self.username} {self.cloth_name} {self.cloth_var} {self.cloth_col_1} {self.cloth_col_2}'
    
    def all_user_datas(self, id):
        datas = []

        for data in UserClothes.objects.filter(user_id = id):
            datas.append({'id': data.id, 'userID': str(data.user_id), 'username': str(data.username), 'cloth_name': str(data.cloth_name), 'cloth_var': str(data.cloth_var), 'cloth_col_1': str(data.cloth_col_1), 'cloth_col_2': str(data.cloth_col_2), 'cloth_img': data.cloth_img})
        
        return datas