from django.db import models
from django.utils import timezone

# Create your models here.


# 계정 테이블
# ID, PW, email, 별명
class User(models.Model):
    _id = models.CharField(max_length=30)
    password = models.CharField(max_length=30)  # 평문으로 데이터가 들어감. 암호화 필수.
    sign_up_date = models.DateTimeField('sing up date')
    nickname = models.CharField(max_length=30)

    def __str__(self):
        return 'id:' + self._id.__str__() \
               + ' pw: ' + self.password.__str__() \
               + ' ni: ' + self.nickname.__str__()

    # 가입
    def create(self):
        self.sign_up_date = timezone.now()
        self.save()

    # 수정
    def update(self):
        pass

    # 탈퇴
    def drop_out(self):
        pass


# 사용자의 옷 데이터를 관리합니다.
# 사용자 고유번호는 장고에 기본 제공되는 _id 속성을 사용합니다.
class UserClothes:
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    pass