import imp
from api import nickinfo, summon_data, actgameinfo
import json
from pprint import pprint

class sumoners:
    def __init__(self, name):
        self.accountId = nickinfo(name)['accountId']
        self.id = nickinfo(name)['id']
        self.name = nickinfo(name)['name']
        self.profileIconId = nickinfo(name)['profileIconId']
        self.puuid = nickinfo(name)['puuid']
        self.revisionDate = nickinfo(name)['revisionDate']
        self.summonerLevel = nickinfo(name)['summonerLevel']
        self.mastery = summon_data(self.id)

class gamedata:
    def __init__(self, id):
        self.gameId = None