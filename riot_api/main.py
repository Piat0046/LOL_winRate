import imp
from name import sumoners
from riot_api.api import actgameinfo
from pprint import pprint
from mongodb import save_mongo, del_mongo

user = sumoners('강찬밥')

def makedata(userid, data): # (유저고유ID, 유저데이터)
    db = {'_id' : userid}
    for i in range(len(data)):
        championId = f"{data[i]['championId']}"
        del data[i]['championId']
        del data[i]['summonerId']
        db[championId] = [data[i]]
    return db