import asyncio
import io
import json
import lzma
import os
import queue

import fastapi
import gridfs
import httpx
from fastapi import FastAPI
from starlette.responses import HTMLResponse, RedirectResponse, StreamingResponse
from starlette.staticfiles import StaticFiles
from lib import DB_uase
from lib.conf import cfgg,tcun
from lib.TM_loop import statrloop

app = FastAPI()
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
    # cfg.cookie=get_cook(co['cookie'])
    bdb=openg('db')
    po=openg('proxe')

    if bdb['v'] =='false':
        dbd = DB_uase.make_client(bdb['ip'],bdb['port'])
        cfg.dbac=dbd[0]
        cfg.db=dbd[1]
        cfg.db_name=bdb['name']


load_config(cfgg)

@app.get("/img")
def image_endpoint(ids,idx):
    # Returns a cv2 image array from the document vector
    i = str(ids)
    a = cfgg.db[cfgg.db_name]
    fs = gridfs.GridFS(a)
    acv = cfgg.db[cfgg.db_name]['pixiv']
    t = acv.find_one({'p_id': i})
    img = t['img'][int(idx)]
    ig = fs.get(img).read()
    imm = lzma.decompress(ig)

    return StreamingResponse(io.BytesIO(imm), media_type="image/png")

if __name__ == "__main__":
    from hypercorn.asyncio import serve
    from hypercorn.config import Config
    try:
        import uvloop
        uvloop.install()
    except ImportError:
        pass

    config = Config()
    config.bind = ["0.0.0.0:9901"]
    config.accesslog = "-"
    config.loglevel = "DEBUG"
    # config.keyfile ="./key.pem"
    # config.certfile="./cert.pem"
    asyncio.run(serve(app, config))
