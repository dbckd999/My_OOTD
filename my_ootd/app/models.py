from django.db import models


# Create your models here.
# 계정 테이블
# ID, PW, email, 별명
class User(models.Model):
    id = models.CharField(max_length=30)
    password = models.CharField(max_length=30)  # 평문으로 데이터가 들어감. 암호화 필수.
    sign_up_date = models.DateTimeField('sing up date')
    nickname = models.CharField(max_length=30)

    # 가입
    # 수정
    # 탈퇴


# 사용자의 옷 데이터를 관리합니다.
# 사용자 고유번호는 장고에 기본 제공되는 _id 속성을 사용합니다.
# 계정을 참고해서 CRD
'''
# 예외처리
#           |내용|                                                                            |기대 결과|
    # 모든 칸에 특수 문자 입력                                                                 -- alert 창이 뜨고 해당 특수문자 삭제
    # 모든 칸 비움                                                                              -- db에 아무것도 올라가지 않음 / 아무런 일도 일어나지 않음
    # db에 데이터가 없는 상태에서 맨 왼쪽 칸 userID 작성 후 나머지 비움                               -- 아무런 일도 일어나지 않음
    # db에 데이터가 있는 상태에서 맨 왼쪽 칸 userID 작성 후 나머지 비움/작성                         -- 해당하는 userID와 관련된 내용 전부 삭제 그 외 아무 일도 일어나지 않음
    # db에 데이터가 있는/없는 상태에서 맨 왼쪽 칸 존재 하지않는 userID 작성 후 나머지 비움            -- 아무런 일도 일어나지 않음
    # db에 데이터가 있는/없는 상태에서 맨 왼쪽 칸 존재 하지않는 userID 작성 후 나머지 작성          -- 아무런 일도 일어나지 않음
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

    pass