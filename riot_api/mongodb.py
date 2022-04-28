from http import client
from xml.dom.minidom import Document
from pymongo import MongoClient
from datetime import datetime
from collections import OrderedDict
import certifi

def save_mongo(basename, name_str, data_name): #데이터베이스, 테이블(Collection), 입력할 데이터
    ##몽고db 계정정보
    HOST = 'cluster0.z5xqr.mongodb.net'
    USER = 'jhp0046'
    PASSWORD = 'qkrwlgns0046'
    DATABASE_NAME = basename
    COLLECTION_NAME = name_str
    MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"
    ca = certifi.where()
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())

    db = client[DATABASE_NAME]
    col = db[COLLECTION_NAME]
    col.insert_one(data_name)
    return print('DB저장완료')

def del_mongo(basename, name_str, data_name): #데이터베이스, 테이블(Collection), 삭제 할 데이터
    ##몽고db 계정정보
    HOST = 'cluster0.z5xqr.mongodb.net'
    USER = 'jhp0046'
    PASSWORD = 'qkrwlgns0046'
    DATABASE_NAME = basename
    COLLECTION_NAME = name_str
    MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"
    ca = certifi.where()
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())

    db = client[DATABASE_NAME]
    col = db[COLLECTION_NAME]
    col.remove(data_name)
    return print('DB삭제완료')



def save_userinfo(data_name): #데이터베이스, 테이블(Collection), 입력할 데이터
    ##몽고db 계정정보
    HOST = 'cluster0.z5xqr.mongodb.net'
    USER = 'jhp0046'
    PASSWORD = 'qkrwlgns0046'
    DATABASE_NAME = 'loldata'
    COLLECTION_NAME = 'userinfo'
    MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"
    ca = certifi.where()
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    db = client[DATABASE_NAME]
    col = db[COLLECTION_NAME]
    data_name['_id']=data_name['id']
    del data_name['id']
    try:
        if data_name['_id'] in list(col.find_one({'_id':data_name['_id']}).values()):
            col.update({'_id':data_name['_id']},data_name)
    except:
        col.insert_one(data_name)
    return print('DB저장완료')

#-----------------------------------------------------------------------------------------
def makedata(userid, data): # (유저고유ID, 유저데이터)
    db = {'_id' : userid}
    for i in range(len(data)):
        championId = f"{data[i]['championId']}"
        del data[i]['championId']
        del data[i]['summonerId']
        db[championId] = [data[i]]
    return db

def save_mastery(data_name): #데이터베이스, 테이블(Collection), 입력할 데이터
    ##몽고db 계정정보
    HOST = 'cluster0.z5xqr.mongodb.net'
    USER = 'jhp0046'
    PASSWORD = 'qkrwlgns0046'
    DATABASE_NAME = 'loldata'
    COLLECTION_NAME = 'user_mastery'
    MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"
    ca = certifi.where()
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())

    db = client[DATABASE_NAME]
    col = db[COLLECTION_NAME]
    try:
        if data_name['_id'] in list(col.find_one({'_id':data_name['_id']}).values()):
            col.update({'_id':data_name['_id']},data_name)
    except:
        col.insert_one(data_name)
    return print('DB저장완료')


#------------------------------------------------------------------------------

def save_log(data):
    HOST = 'cluster0.z5xqr.mongodb.net'
    USER = 'jhp0046'
    PASSWORD = 'qkrwlgns0046'
    DATABASE_NAME = 'loldata'
    COLLECTION_NAME = 'search_log'
    MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"
    ca = certifi.where()
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    db = client[DATABASE_NAME]
    col = db[COLLECTION_NAME]
    count = col.find().count()
    data.update({'_id' : count+1, 'time' : datetime.now()})
    data.move_to_end('time', False)
    col.insert(data)
    return print('DB저장완료')



class logdata():
    def __init__(self):   
        self.doc = OrderedDict()
    
    def insert(self, dict, Bool=False):
        if Bool is False:
            self.doc.update(dict)
        else:
            self.doc.update(dict)
            save_log(self.doc)
# def logdata(data):
#     dic = {'_id' : 'null',
#            'Input_name' : 'null',
#            'page_response' : 'null',
#            'Ingame' : 'null',
#            '1p_id' : 'null',
#            '1p' : 'null',
#            '2p_id' : 'null',
#            '2p' : 'null',
#            '3p_id' : 'null',
#            '3p' : 'null',
#            '4p_id' : 'null',
#            '4p' : 'null',
#            '5p_id' : 'null',
#            '5p' : 'null',
#            '6p_id' : 'null',
#            '6p' : 'null',
#            '7p_id' : 'null',
#            '7p' : 'null',
#            '8p_id' : 'null',
#            '8p' : 'null',
#            '9p_id' : 'null',
#            '9p' : 'null',
#            '10p_id' : 'null',
#            '10p' : 'null',
#            }
    