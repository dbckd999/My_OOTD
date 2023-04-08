from django.db import models
from django.utils import timezone

# Create your models here.


# 계정 테이블
# ID, PW, email, 별명
class User(models.Model):
    # Django에서 자동으로 생성되는 id가 아니고, 사용자가 입력해 사용하는것입니다.
    _id = models.CharField(max_length=30)
    password = models.CharField(max_length=30, null=False)  # 평문으로 데이터가 들어감. 암호화 필수.
    sign_up_date = models.DateTimeField('sing up date', null=False)
    nickname = models.CharField(max_length=30, null=False)

    def __str__(self):
        return 'id:' + self._id.__str__() \
               + ' pw: ' + self.password.__str__() \
               + ' ni: ' + self.nickname.__str__()

    # 가입
    def create(self):
        self.sign_up_date = timezone.now()
        self.save()

    # 닉네임 변경
    # def chagne_nickname(self):
    #     self.save(update_fields=self.nickname)

    # 비밀번호 변경
    # def change_password(self):
    #     self.save(update_fields=self.password)

    # 탈퇴
    # id를 받아 계정을 삭제
    def drop_out(self):
        pass

    # 들어온 id, pw를 확인하고 계정의
    def login(self):
        pass


# 사용자의 옷 데이터를 관리합니다.
# 사용자 고유번호는 장고에 기본 제공되는 _id 속성을 사용합니다.
# 계정을 참고해서 CRD
'''
# 예외처리
#           |내용|                                                                            |기대 결과|
    # 모든 칸에 특수 문자 입력                                                                 -- alert 창이 뜨고 해당 특수문자 삭제
    # 모든 칸 비움                                                                              -- db에 아무것도 올라가지 않음 / 아무런 일도 일어나지 않음
    # 맨 왼쪽 칸을 제외한 나머지 모든 칸 입력                                                   -- db에 입력한 데이터 저장
    # 맨 왼쪽 칸을 제외한 나머지 모든 칸 중 한 칸을 빼고 입력                                   -- db에 데이터가 저장되지 않음
    # db에 데이터가 없는 상태에서 맨 왼쪽 칸에 존재하는/하지않는 userID 작성 후 나머지 비움           -- 아무런 일도 일어나지 않음
    # db에 데이터가 있는 상태에서 맨 왼쪽 칸에 존재하는 userID 작성 후 나머지 비움/작성             -- 해당하는 userID와 관련된 데이터 전부 삭제 / db에 데이터가 저장되는 현상 발생하지 않음
    # db에 데이터가 있는/없는 상태에서 맨 왼쪽 칸에 존재하지않는 userID 작성 후 나머지 비움            -- 아무런 일도 일어나지 않음
    # db에 데이터가 있는/없는 상태에서 맨 왼쪽 칸에 존재하지않는 userID 작성 후 나머지 작성          -- 아무런 일도 일어나지 않음
    # 여기에 userID 입력 에 아무것도 입력하지 않았을 때 (주석만 넣었을 때)                            -- 조회창에 아무것도 나오지 않음
''' 

class UserClothes(models.Model):
    #user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    tmp_userid = models.CharField(max_length=10) # 임시 계정
    cloth_name = models.CharField(max_length=50) # 옷 이름
    cloth_var = models.CharField(max_length=30) # 옷 종류 (자켓, 셔츠 등)
    cloth_col_1 = models.CharField(max_length=30) # 옷 색깔 1
    cloth_col_2 = models.CharField(max_length=30) # 옷 색깔 2

    def __str__(self):
        return f'{self.tmp_userid} {self.cloth_name} {self.cloth_var} {self.cloth_col_1} {self.cloth_col_2}'