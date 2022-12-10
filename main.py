import asyncio
import json
import os
import queue

import fastapi
import httpx
from fastapi import FastAPI
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.staticfiles import StaticFiles
from lib import DB_uase
from lib.conf import cfgg,tcun
from lib.TM_loop import statrloop
# from lib.don import set_cookie_a
#'http://127.0.0.1:8889'
def get_cook(sttrr):
    cookies1 = httpx.Cookies()
    c_list = sttrr.split(';')
    for c in c_list:
        # print(c)
        ds = c.split('=', maxsplit=1)
        # print(ds)
        cookies1.set(ds[0].strip(), ds[1].strip())
    return cookies1


def load_config(cfg:tcun):
    def openg(f):
        with open('./config/'+f,'r',encoding='utf-8') as f:
            return json.loads(f.read())
    cg=openg('config.json')
    cfg.maxT=cg['maxT']
    cfg.wait=cg['wait']
    cfg.sc_time=cg['sc_time']
    co=openg('cookies')
    cfg.uid=co['uid']
    cfg.cookie=get_cook(co['cookie'])
    bdb=openg('db')
    po=openg('proxe')

    if bdb['v'] =='false':
        dbd = DB_uase.make_client(bdb['ip'],bdb['port'])
        cfg.dbac=dbd[0]
        cfg.db=dbd[1]
        cfg.db_name=bdb['name']

    cfg.proxy='http://'+po['ip']+':'+po['port']





def openf():
    with open('./html/fi.vue','r',encoding='utf-8') as f:
        ddd=f.read()
    return ddd

app = FastAPI()
app.mount("/js_css", StaticFiles(directory="./js_css"), name="js_css")

@app.get("/addt", response_class=HTMLResponse)
async def mainn(types,item):
    # print(item)
    # json.loads(item)
    qf.put({'type':types,'item':json.loads(item)})

@app.get("/", response_class=HTMLResponse)
async def mainn():
    if fistr==1:
        return RedirectResponse("/first/")


@app.get("/first/", response_class=HTMLResponse)
async def first():
    if fistr==0:
        return RedirectResponse("/")
    return openf()
@app.get("/first_api/", )
async def first_api(p_ip:str,P_p:str,db_ip:str,db_port:str,db_name:str,cookie:str,T_num:str,T_time:str,sc_timr:str,verify:str,uid:str,DB_u:str=None,DB_p:str=None):
    # p_ip:str,P_p:str,db_ip:str,db_port:str,db_name:str,cookie:str,T_num:str,T_time:str,sc_timr:str,verify:str,DB_u:str=None,DB_p:str=None
    # print(p_ip,P_p,db_ip,db_port,db_name,cookie,T_num,T_time,sc_timr,verify)
    if fistr==0:
        return '11111'
    make_file(p_ip,P_p,db_ip,db_port,db_name,cookie,T_num,T_time,sc_timr,verify,uid,DB_u,DB_p)
    exit(0)

    return 'aaaaa'

def make_file(p_ip,P_p,db_ip,db_port,db_name,cookie,T_num,T_time,sc_timr,verify,uid,DB_u:str=None,DB_p:str=None,ly=3):
    db_json={'ip':db_ip,'port':db_port,'name':db_name,'v':verify,'p':DB_p,'u':DB_u}
    p_json = {'ip': p_ip, 'port': P_p}
    cookies={'uid':uid,'cookie':cookie}
    config={'maxT':T_num,'wait':T_time,'sc_time':sc_timr,'ly':ly}

    def openn(j,n):
        jsonn=json.dumps(j)
        with open('./config/'+n,'w',encoding='utf-8' ) as f:
            f.write(jsonn)
    openn(db_json,'db')
    openn(p_json, 'proxe')
    openn(cookies, 'cookies')
    openn(config, 'config.json')
    pass



if __name__ == "__main__":
    from hypercorn.asyncio import serve
    from hypercorn.config import Config
    try:
        import uvloop
        uvloop.install()
    except ImportError:
        pass
    fistr = 0
    if not os.path.exists('./config'):
        os.makedirs('./config')
    if not os.path.exists('./config/config.json'):
        fistr = 1
    # cfgg=tcun()
    if fistr==0:

        load_config(cfgg)
        qf=queue.Queue(100)
        qf1 = queue.Queue(10000)
        qf2 = queue.Queue(1000)
        qf3 = queue.Queue(1000)
        qf4 = queue.Queue(1000)
        qf5= queue.Queue(1000)
        statrloop(qf,qf1,qf2,qf3,qf4,qf5)
        print(cfgg.proxy)
    config = Config()
    config.bind = ["0.0.0.0:9900"]
    config.accesslog = "-"
    config.loglevel = "DEBUG"
    # config.keyfile ="./key.pem"
    # config.certfile="./cert.pem"
    asyncio.run(serve(app, config))
