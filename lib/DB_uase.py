import asyncio
import lzma
import time

import motor.motor_asyncio
from pymongo import MongoClient
import zlib
import bz2
# lzma.compress(b, preset=5)
#6级别lzma压缩
# client = motor.motor_asyncio.AsyncIOMotorClient('192.168.1.112', 27017)

def make_client(ips='127.0.0.1',port=27017,u=None,p=None,):
    ui=0
    pi=0
    if u is not None:
        ui=1
    if p is not None:
        pi=1
    if ui==pi:
        if ui==0:
            return( motor.motor_asyncio.AsyncIOMotorClient(f'mongodb://{ips}:{port}'),MongoClient(f'mongodb://{ips}:{port}'))
        else:
            return (motor.motor_asyncio.AsyncIOMotorClient(f'mongodb://{u}:{p}@{ips}:{port}'),MongoClient(f'mongodb://{ips}:{port}'))
    else:
        raise Exception('errrr')

class get_db:
    def __init__(self,ip,Q_err,db_name='pi',port=27017,u=None,p=None):
        self.eng=make_client(ips=ip,port=port,u=u,p=p)
        self.err_q=Q_err
        self.dbac = self.eng[0][db_name]
        self.db = self.eng[1][db_name]

    def get_dbac(self):
        return self.dbac
    def get_db(self):
        return self.db

def prp_data(pid,img,types,intruduct,tag,tag_fy,author,title,age,add_time=None,farm_time=None,org_zip=None,context=None,):
    if add_time is  None:
        add_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    if farm_time is None:
        farm_time=''
    if org_zip is None:
        org_zip =''
    if context is None:
        context = ''
    for i in author:
        k=i
        author={str(k):author[i]}

    return {'p_id':str(pid),'img':img,'type':types,'intruduct':intruduct,'tag':tag,'tag_fy':tag_fy,'author':author
        ,'title':title,'age':age
        ,'add_time':add_time,
            'farm_time':farm_time,'org_zip':org_zip,'context':context

            }
# def initdb_ac(item,db):
#     async def do_insert():
#         # document = {'key': 'value'}
#         result = await db.insert_one(item)  # insert_one只能插入一条数据
#         print('result %s' % repr(result.inserted_id))
#
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(do_insert())
#
# client = make_client('192.168.1.112', 27018)[0]
# db1 = client['test_database']
# collection = db1['test_collection']
# document = prp_data('212232',[232,2323],2,323,[232,323,32],[{1:2}, {2: 3}],2,'2323','f3csf')
# document={'p_id': '212232', 'img': [232, 2323], 'type': 2, 'intruduct': 323, 'tag': [232, 323, 32], 'tag_fy': [{'22': 2}, {'33': 3}], 'author': 2, 'title': '2323', 'age': 'f3csf', 'add_time': '2022-12-03 19:52:09', 'farm_time': '', 'org_zip': '', 'context': ''}
#
# print(document)
# initdb_ac(document,collection)
#
#
#
#



# client = MongoClient('192.168.1.112', 27018)
# client = make_client('192.168.1.112', 27018)
# db = client['test_database']
# collection = db['test_collection']
# document = {'key': 'value'}
# result = collection.insert_one(document)  # insert_one只能插入一条数据
# print(f'result {repr(result.inserted_id)}')


# async def do_insert():
#     document = {'key': 'ddd'}
#     result = await db.test_collection.insert_one(document)  # insert_one只能插入一条数据
#     print(f'result {repr(result.inserted_id)}')

# async def do_insert():
#     document = {'key': 'ddd'}
#     result = await collection.find_one() # insert_one只能插入一条数据
#     # print(result)
#
#     with open('sss.gif','wb') as f:
#         f.write(result['img'][0])
#
#
#     for i in range(10):
#
#         with open(f'lzma{str(i)}.gif', 'wb') as f:
#             f.write(lzma.compress(result['img'][0], preset=i))
#
# # do_insert()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(do_insert())
# with open('lzma1111.gif', 'wb') as f:
#     f.write(lzma.compress(result['img'][0], preset=i))
# for i in range(10):
#     loop.run_until_complete(do_insert())
# print('aaa')