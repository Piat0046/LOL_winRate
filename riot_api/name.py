from riot_api.api import *
import json
from pprint import pprint

class sumoners:
    def __init__(self, info):
        self.accountId = info['accountId']
        self.id = info['id']
        self.name = info['name']
        self.profileIconId = info['profileIconId']
        self.puuid = info['puuid']
        self.revisionDate = info['revisionDate']
        self.summonerLevel = info['summonerLevel']
        self.mastery = summon_data(self.id)

class gamedata:
    def __init__(self, id):
        self.gameId = None