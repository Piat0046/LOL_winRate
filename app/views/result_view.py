from flask import Flask, render_template, request, Blueprint
import pickle
import psycopg2

bp = Blueprint('predict', __name__, url_prefix='/')

@bp.route('/result', methods=['POST', 'GET'])
def result(champ1=None):

    import requests
    import json
    import time
    import pprint
    import copy
    from riot_api.mongodb import save_mastery, save_mongo, makedata, save_userinfo, save_log,logdata
    from riot_api.api import nickinfo, url_check
    from riot_api.name import sumoners
    from riot_api.model import model
    from urllib import parse

    # log 기록 클래스 선언
    log_class = logdata()

    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        # sel_champ = set()
        # sel_nick = set()
        # for i in range(1,11):
        #     sel_champ.add(request.args.get('champ'+f'{i}'))
        # for i in range(1,11):
        #     sel_nick.add(request.args.get('champ'+f'{i}'+'_nick'))
        
        # sel_champ = list(sel_champ)
        # sel_nick = list(sel_nick)
        # num = len(sel_champ)

        request_header = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
                            "Accept-Language": "ko,en-US;q=0.9,en;q=0.8,es;q=0.7",
                            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                            "Origin": "https://developer.riotgames.com",
                            "X-Riot-Token": 'RGAPI-51930c7c-d051-44a4-93e8-fcbb592beb5f'
                        }

        ## Get user's nickname
        nick = request.form['username']
        print(nick)
        # Delete space from SummonersNick
        nick = nick.replace(" ", "")
        log_class.insert({"Input_name" : nick})
        # get nickname api
        url_nick = f'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{parse.quote_plus(nick)}'        
        # checking url
        m = url_check(url_nick) 
        ## Start Playing win rate
        if nick == "": # if No enter nickname
            m = '닉네임을 입력하세요'
            log_class.insert({"result" : m})
            save_log(log_class.doc)

        else:
            if m == 'fail': # if Not fount summoners
                m = '소환사를 찾을 수 없습니다.'
                log_class.insert({"result" : m})
                save_log(log_class.doc)
                print('소환사를 찾을 수 없습니다.')

            elif m == 'pass': # if get Summoners info
                log_class.insert({"result" : m})
                user_info_data = nickinfo(nick) #유저정보 적재
                user = sumoners(user_info_data) #유저정보 객체화
                save_userinfo(user_info_data) # 유저정보 mongodb저장
                save_mastery(makedata(user.id, user.mastery)) # 유저 챔피언 정보 mongodb저장

                nick_to_id = requests.get(url_nick, headers=request_header).json()
                input_id = nick_to_id['id']
                url_game = f'https://kr.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{input_id}'
                m = url_check(url_game)
                
                if m == 'fail': # if Not playing game
                    m = '소환사가 게임중이 아닙니다'
                    game = False
                    log_class.insert({"ingame" : game})
                    save_log(log_class.doc)
                    print('소환사가 게임중이 아닙니다')

                elif m == 'pass': # found gamedata
                    data = requests.get(url_game, headers=request_header).json()
                    game = True
                    log_class.insert({"ingame" : game})
                    dic = []
                    log_data = []  # [ID, SummonersNickname, Nowplay(True/False)]

                    ## Get PlayerData
                    for i in range(0,10):
                        summoner_Id = data['participants'][i]['summonerId']
                        log_data.append(summoner_Id)
                        champ_id = data['participants'][i]['championId']
                        log_data.append(champ_id)
                        champ_status_url = f"https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_Id}/by-champion/{champ_id}"
                        m = url_check(champ_status_url)
                        print(m)
                        champ_status = requests.get(champ_status_url, headers=request_header).json()
                        champ_point = champ_status['championPoints']
                        dic.append(champ_id)
                        dic.append(champ_point)
                        log_data.append(champ_point)

                    doc = list()
                    keys = list(map(lambda x: [f'{x}p_id', f'{x}p', f'{x}score'], range(1,11)))
                    list(map(lambda x : doc.extend(x), keys))
                    doc = {key: value for key, value in zip(doc, log_data)}
                    log_class.insert(doc, True)

                    model(dic)
                    
    return render_template('result.html', username = nick, m = m)
