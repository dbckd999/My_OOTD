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
base_time = '0200'

url += f'serviceKey={serviceKey}&numOfRows={numOfRows}&pageNo={pageNo}&base_date={base_date}&base_time={base_time}&nx={nx}&ny={ny}'

# 오늘 [기온], 최고, 최저기온, 강수확률, 풍속 딕셔너리를 반환
def weather() -> dict:
    cont = requests.get(url)
    tree = ElementTree.fromstring(cont.text)
    doc = {
        # 'TMP': [],
        'TMX': -999,
        'TMN': 999,
        'POP': -1,
        'WSD': -1
    }

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

    # 기온
    # for item in tree.findall(f".//item[fcstDate='{base_date}'][category='TMP']"):
    #     doc['TMP'].append(float(item.find('fcstValue').text))

    # 최고 기온
    for tmx in tree.findall(f".//item[fcstDate='{base_date}'][category='TMX']"):
        doc['TMX'] = float(tmx.find('fcstValue').text)
    # doc['TMX'] = float(tree.find(f".//item[fcstDate='{base_date}'][category='TMX']").find('fcstValue').text)

    # 최저 기온
    for tmx in tree.findall(f".//item[fcstDate='{base_date}'][category='TMN']"):
        doc['TMN'] = float(tmx.find('fcstValue').text)
    # doc['TMN'] = float(tree.find(f".//item[fcstDate='{base_date}'][category='TMN']").find('fcstValue').text)

    # 강수확률
    for item in tree.findall(f".//item[fcstDate='{base_date}'][category='POP']"):
        if doc['POP'] < float(item.find('fcstValue').text):
            doc['POP'] = float(item.find('fcstValue').text)

    # 최고 풍속
    for item in tree.findall(f".//item[fcstDate='{base_date}'][category='WSD']"):
        if doc['WSD'] < float(item.find('fcstValue').text):
            doc['WSD'] = float(item.find('fcstValue').text)

    # 하늘상태(SKY) 코드 : 맑음(1), 구름많음(3), 흐림(4)
    sky_stack = [0, 0, 0]
    for item in tree.findall(f".//item[fcstDate='{base_date}'][category='SKY']"):
        if int(item.find('fcstValue').text) == 1:
            sky_stack[0] += 1
        elif int(item.find('fcstValue').text) == 3:
            sky_stack[1] += 1
        elif int(item.find('fcstValue').text) == 4:
            sky_stack[2] += 1
        else:
            print("Undefined SKY code")
    doc['SKY_st'] = sky_stack

    # 강수형태(PTY) 코드 : 없음(0), 비(1), 비/눈(2), 눈(3), 소나기(4)
    pty_stack = [0, 0, 0, 0, 0]
    for item in tree.findall(f".//item[fcstDate='{base_date}'][category='PTY']"):
        pty_stack[int(item.find('fcstValue').text)] += 1
    doc['PTY_st'] = pty_stack

    return doc


# 하늘상태(SKY) 코드 : 맑음, 구름많음, 흐림
# 강수형태(PTY) 코드 : 없음, 비, 비/눈, 눈, 소나기
def select_weather_icon_name(sky: list, pty: list) -> str:
    icon_name = ''
    # sky             맑음       / 구름많음   / 흐림
    sky_icon_name = ['NB01.png', 'NB03.png', 'NB04.png']
    # pty            # 비       / 비 또는 눈 / 눈 또는 비 / 눈       / 소나기
    pty_icon_name = ['NB08.png', 'NB12.png', 'NB13.png', 'NB11.png', 'NB07.png']

    if pty.index(max(pty)) == 0:
        icon_name = sky_icon_name[sky.index(max(sky))]
    else:
        icon_name = pty_icon_name[pty.index(max(pty))]

    # print(icon_name)
    return icon_name
