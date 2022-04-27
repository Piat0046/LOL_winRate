import imp
from name import sumoners
from api import actgameinfo
from pprint import pprint
from mongodb import save_mongo, del_mongo

user = sumoners('강찬밥')

def makedata(userid, data):
    db = {'_id' : userid}
    for i in range(len(data)):
        championId = f"{data[i]['championId']}"
        del data[i]['championId']
        db[championId] = [data[i]]

    return db

del_mongo('loldata', 'userinfo', {'_id':"GNi7hk7xYv5SHKJib4zkR5MLJW6xwHE_ksotqzSRYQLPTg"})

#print(makedata(user.id, user.mastery))