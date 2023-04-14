"""
기상 데이터를 관리합니다.

serviceKey	인증키
numOfRows	한 페이지 결과 수
pageNo	페이지 번호
dataType	응답자료형식
base_date	발표일자
base_time	발표시각
nx	예보지점 X 좌표
ny	예보지점 Y 좌표

"""

serviceKey = 'om5Yy5MnYGk4Gvst9OAO%2BO2QB8RpxYEjR5KyIzp1S1T7Tai8%2FtF6ybNrxyWw8sHxPWxdApz1WlVeWCwMzZLiIQ%3D%3D'

url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?'

url += 'serviceKey=' + serviceKey + '&'

# 대충 현재위치를 받는 기능
nx = 0
ny = 0

