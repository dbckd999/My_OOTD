from django.db import models
from django.contrib.auth.models import User

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
    # tmp_userid = models.CharField(max_length=10) # 임시 계정

    user_id = models.ForeignKey(User, on_delete=models.CASCADE) # 유저 고유 번호
    username = models.CharField(max_length=50, null=True) # 유저이름
    cloth_name = models.CharField(max_length=50) # 옷 이름
    cloth_var = models.CharField(max_length=30) # 옷 종류 (자켓, 셔츠 등)
    cloth_col_1 = models.CharField(max_length=30) # 옷 색깔 1
    cloth_col_2 = models.CharField(max_length=30) # 옷 색깔 2
    #cloth_img = models.ImageField(null=True)

    def __str__(self):
        return f'{self.user_id} {self.username} {self.cloth_name} {self.cloth_var} {self.cloth_col_1} {self.cloth_col_2}'
    
    def all_user_datas(self, id):
        datas = []

        for data in UserClothes.objects.filter(user_id = id):
            datas.append({'id': data.id, 'userID': str(data.user_id), 'username': str(data.username), 'cloth_name': str(data.cloth_name), 'cloth_var': str(data.cloth_var), 'cloth_col_1': str(data.cloth_col_1), 'cloth_col_2': str(data.cloth_col_2)})
        
        return datas