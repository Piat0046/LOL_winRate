from http import client
from xml.dom.minidom import Document
from pymongo import MongoClient
import certifi

def save_mongo(basename, name_str, data_name):
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

def del_mongo(basename, name_str, data_name):
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

def mk_log(data):
    pass