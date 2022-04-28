from flask import Flask, render_template, request, Blueprint
import pickle
import psycopg2

from riot_api.mongodb import save_log

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index(champ1=None):
    gameId_list = []
    name = gameId_list
    return render_template('index.html',  name = name, champ1=champ1)


@bp.route('/result', methods=['POST', 'GET'])
def result(champ1=None):
    
    ## heroku-PostgresSQL 연결
    import psycopg2
    import requests
    import json
    import time
    import pprint
    import pandas as pd
    import copy
    from riot_api.mongodb import save_mastery, save_mongo, makedata, save_userinfo, logdata
    from riot_api.api import nickinfo, url_check
    from riot_api.name import sumoners
    from urllib import parse

    # log 기록 클래스 선언
    log_class = logdata()

    print('1')
    conn = psycopg2.connect(
                            host="ec2-52-86-2-228.compute-1.amazonaws.com",
                            database="dd5g8l3ltkq7fu",
                            user="rxhgazotbubwqj",
                            password="8b76cbfb2cf1c6e4591ccc8eff75d95f39e7873128b563d57666c849cbff0af7"
                            )   
    cur = conn.cursor()
    cur.execute("SELECT COUNT('ID') from Log_data") # 로그데이터 저장을 위한 SQL호출
    count = cur.fetchone()[0] # 마지막 저장 로그기록번호


    if request.method == 'POST':
        pass

    elif request.method == 'GET':
        sel_champ = set()
        sel_nick = set()
        for i in range(1,11):
            sel_champ.add(request.args.get('champ'+f'{i}'))
        for i in range(1,11):
            sel_nick.add(request.args.get('champ'+f'{i}'+'_nick'))
        
        sel_champ = list(sel_champ)
        sel_nick = list(sel_nick)
        num = len(sel_champ)

        request_header = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
                            "Accept-Language": "ko,en-US;q=0.9,en;q=0.8,es;q=0.7",
                            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                            "Origin": "https://developer.riotgames.com",
                            "X-Riot-Token": 'RGAPI-51930c7c-d051-44a4-93e8-fcbb592beb5f'
                        }

        ## Get user's nickname
        nick = request.args.get('username')

        

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
            val = [count+1, nick]
            print(count, type(count))
            print(nick, type(nick))
            cur.execute(f"""INSERT INTO log_data("ID", "Input_name")
            VALUES (%s,%s);""", val)
            conn.commit()
            log_class.insert({"result" : m})
            save_log(log_class.doc)

        else:
            if m == 'fail': # if Not fount summoners
                m = '소환사를 찾을 수 없습니다.'
                cur.execute(f"""INSERT INTO log_data("ID", "Input_name")
                VALUES ({count+1},'{nick}');""")
                conn.commit()
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
                    cur.execute(f"""INSERT INTO log_data("ID", "Input_name", "Ingame")
                    VALUES ({count+1},'{nick}',{game});""")
                    conn.commit()
                    log_class.insert({"ingame" : game})
                    save_log(log_class.doc)
                    print('소환사가 게임중이 아닙니다')

                elif m == 'pass': # found gamedata
                    data = requests.get(url_game, headers=request_header).json()
                    game = True
                    log_class.insert({"ingame" : game})
                    dic = []
                    log_data = [count+1, nick, game]  # [ID, SummonersNickname, Nowplay(True/False)]

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

                    

                    ## Write ingame player data at Log
                    cur.execute(f"""INSERT INTO log_data("ID", "Input_name","Ingame","1pick_id","1pick","1score","2pick_id","2pick","2score",
                                                            "3pick_id","3pick","3score","4pick_id","4pick","4score","5pick_id","5pick","5score",
                                                            "6pick_id","6pick","6score","7pick_id","7pick","7score","8pick_id","8pick","8score",
                                                            "9pick_id","9pick","9score","10pick_id","10pick","10score")
                                                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""", log_data)
                    conn.commit()

                    doc = list()
                    keys = list(map(lambda x: [f'{x}p_id', f'{x}p', f'{x}score'], range(1,11)))
                    list(map(lambda x : doc.extend(x), keys))
                    log_data2 = copy.deepcopy(log_data)
                    del log_data2[0:3]
                    {key: value for key, value in zip(doc, log_data2)}



                    import pickle
                    import pandas as pd
                    from lightgbm import LGBMClassifier, plot_importance
                    from xgboost import XGBClassifier

                    model = None

                    with open('model4.pkl', 'rb') as file:
                        model = pickle.load(file)

                    columns = ['1', '1score', '2', '2score', '3', '3score', '4', '4score', '5', '5score', '6', '6score', '7', '7score', '8', '8score', '9', '9score', '10', '10score']
                    df = pd.DataFrame(columns = columns)
                    input_data = {
                                '1' : dic[0],
                                '1score' : dic[1],
                                '2' : dic[2],
                                '2score' :dic[3],
                                '3' : dic[4],
                                '3score' : dic[5],
                                '4' : dic[6],
                                '4score' : dic[7],
                                '5' : dic[8],
                                '5score' : dic[9],
                                '6' : dic[10],
                                '6score' : dic[11],
                                '7' : dic[12],
                                '7score' : dic[13],
                                '8' : dic[14],
                                '8score' : dic[15],
                                '9' : dic[16],
                                '9score' : dic[17],
                                '10' : dic[18],
                                '10score' : dic[19],
                                }
                    X_test = df.append(input_data, ignore_index=True)
                    X_test = X_test.astype(int)
                    y_pred = list(model.predict(X_test))[0]
                    c=model.predict_proba(X_test).reshape(-1,1)
                    
                    blue_team = int(list(c[0])[0]*100)
                    red_team = int(list(c[1])[0]*100)
                    
                    if y_pred == 200:
                        y_pred = '레드팀'
                    else:
                        y_pred = '블루팀'

                    m = f'예상승리팀 : {y_pred},{"     "}블루팀={blue_team}%, 레드팀{red_team}%'

    cur.close
    conn.close

    return render_template('result.html', nick = sel_nick, champ=sel_champ, num = num, username = nick, m = m)
