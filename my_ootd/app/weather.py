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

맑음       0 ~ 5
구름많음    6 ~ 8
흐림       9 ~ 10
"""

import requests
from xml.etree import ElementTree
import time
import re

# base url
url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?'

# key
serviceKey = 'om5Yy5MnYGk4Gvst9OAO%2BO2QB8RpxYEjR5KyIzp1S1T7Tai8%2FtF6ybNrxyWw8sHxPWxdApz1WlVeWCwMzZLiIQ%3D%3D'

numOfRows = 809
pageNo = 1

# 대충 현재위치를 받는 기능
nx = 90
ny = 90
base_date = time.strftime('%Y%m%d')
# 최저기온: 2시, 최고기온: 2, 5, 8, 11시 갱신
base_time = '0500'

url += 'serviceKey=' + serviceKey + '&numOfRows=' + str(numOfRows) + '&pageNo=' + str(
    pageNo) + '&base_date=' + base_date + '&base_time=' + base_time + '&nx=' + str(nx) + '&ny=' + str(ny)


# 오늘 기온, 최고, 최저기온, 강수확률, 풍속 딕셔너리를 반환합니다.
def weather() -> dict:
    cont = requests.get(url)
    open('res.xml', 'w').write(cont.text)

    tree = ElementTree.fromstring(cont.text)
    doc = {}

    means = {
        'POP': '강수확률'
        , 'PTY': '강수형태'
        , 'PCP': '1시간 강수량'
        , 'REH': '습도\t'
        , 'SNO': '1시간 신적설'
        , 'SKY': '하늘상태'
        , 'TMP': '1시간 기온'
        , 'TMN': '일 최저기온'
        , 'TMX': '일 최고기온'
        , 'UUU': '풍속(동서성분)'
        , 'VVV': '풍속(남북성분)'
        , 'WAV': '파고\t'
        , 'VEC': '풍향\t'
        , 'WSD': '풍속\t'
    }

    # !! 시간별로 정렬되어 정보가 들어오지 않는다. 정렬 해야함 !!
    for item in tree.iter('item'):
        tag = item.find('category').text
        # print(f"{means[tag]}\t {item.find('fcstValue').text}")

        if item.find('category').text in doc:
            doc[tag].append(item.find('fcstValue').text)
        else:
            doc[tag] = [item.find('fcstValue').text]

    # print(doc)

    for li in doc:
        print(li + ':' + str(doc[li]))
    print()

    # meta data
    doc['metadata'] = {
        'numOfRows': tree.find('.//numOfRows').text
        , 'pageNo': tree.find('.//pageNo').text
        , 'totalCount': tree.find('.//totalCount').text
    }

    # print(doc['metadata'])
    return {
        'TMP': max(list(map(int, doc['TMP'])))
        , 'TMX': max(list(map(float, doc['TMX'])))
        , 'TMN': max(list(map(float, doc['TMN'])))
        , 'POP': max(list(map(int, doc['POP'])))
        , 'WSD': max(list(map(float, doc['WSD'])))
    }


def select_weather_icon():
    file_name = [
        'NB02.png',  # 구름조금
        'NB03.png',  # 구름많음
        'NB04.png',  # 흐림
        'NB07.png',  # 소나기
        'NB08.png',  # 비
        'NB11.png',  # 눈
        'NB12.png',  # 비 또는 눈
        'NB13.png',  # 눈 또는 비
        'NB14.png',  # 천둥번개
        'NB15.png',  # 안개
        'NB16.png',  # 황사
        'NB17.png',  # 박무(엷은 안개)
        'NB18.png',  # 연무
        'NB20.png',  # 가끔(한때) 비 또는 비
        'NB21.png',  # 가끔(한때) 눈 또는 눈
        'NB22.png',  # 가끔(한때) 비, 또는 눈
        'NB23.png'  # 가끔(한때) 눈 또는 비
    ]

