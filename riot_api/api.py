import requests
import json
import time
from urllib import parse, request

request_header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
                "Accept-Language": "ko,en-US;q=0.9,en;q=0.8,es;q=0.7",
                "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://developer.riotgames.com",
                "X-Riot-Token": 'RGAPI-51930c7c-d051-44a4-93e8-fcbb592beb5f'
                }

def nickinfo(name):
    url = f'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{parse.quote_plus(name)}'
    info = requests.get(url, headers = request_header).json()
    return info


def actgameinfo(id):
    url = f'https://kr.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{id}'
    info = requests.get(url, headers = request_header).json()
    return info


def summon_data(id):
    url = f"https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{id}"
    info = requests.get(url, headers = request_header).json()
    return info


def url_check(url):
    r = requests.get(url, headers=request_header)
    if r.status_code == 200: # response가 정상이면 바로 맨 밑으로 이동하여 정상적으로 코드 실행
        m = 'pass'
        print('pass')
        pass
    elif r.status_code == 403:
        print('pass')
        m = 'pass'
    elif r.status_code == 429:
        print('api cost full : infinite loop start')
        start_time = time.time()
        
        while True: # 429error가 끝날 때까지 무한 루프
            if r.status_code == 429:

                print('try 10 second wait time')
                time.sleep(10)
                r = requests.get(url, headers=request_header)
                print(r.status_code)

            elif r.status_code == 200: #다시 response 200이면 loop escape
                print('total wait time : ', time.time() - start_time)
                print('recovery api cost')
                m = 'pass'
                break

            else:
                m = 'fail'
                break
    
    else:
        m = 'fail'

    return m

