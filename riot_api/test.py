# from api import *
# from mongodb import *
# from pprint import pprint
# from name import sumoners
# from http import client
# from xml.dom.minidom import Document
# from pymongo import MongoClient
# import time
# import certifi

# data_name = nickinfo('핫상범')
# user = sumoners(data_name)

# HOST = 'cluster0.z5xqr.mongodb.net'
# USER = 'jhp0046'
# PASSWORD = 'qkrwlgns0046'
# DATABASE_NAME = 'loldata'
# COLLECTION_NAME = 'userinfo'
# MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"
# ca = certifi.where()
# client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
# db = client[DATABASE_NAME]
# col = db[COLLECTION_NAME]
# data = ["1pick_id","1pick","1score","2pick_id","2pick","2score","3pick_id","3pick","3score","4pick_id","4pick","4score","5pick_id","5pick","5score",
# "6pick_id","6pick","6score","7pick_id","7pick","7score","8pick_id","8pick","8score",
# "9pick_id","9pick","9score","10pick_id","10pick","10score"]
#a = [f'{x}p_id', f"{y}pick",f"{z}score" for x,y,z in zip(range(1,11),range(1,11),range(1,11))]
# a = [f'{x}p_id' for x in range(1,11)]
# b = [f'{x}p' for x in range(1,11)]
# c = [f'{x}score' for x in range(1,11)]

keys = list(map(lambda x: [f'{x}p_id', f'{x}p', f'{x}score'], range(1,11)))
doc = list()
list(map(lambda x : doc.extend(x), keys))
del doc[0:3]
print(doc)

