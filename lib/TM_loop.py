import random
import threading
import time

from lib import T_pool
import queue
from lib import inst_tool as ist
from lib.don import done, id_G, run_Gid
from lib.conf import cfgg
basep = './data/wait/'
from gridfs import GridFS
import gridfs
def cad(obj):
    li=[]
    ogj=obj
    imgg=obj['img']
    for i in imgg:
        a = cfgg.db[cfgg.db_name]
        fs = gridfs.GridFS(a)
        bcd = fs.put(i)
        li.append(bcd)
    if obj['org_zip']!='':
        a = cfgg.db[cfgg.db_name]
        fs = gridfs.GridFS(a)
        bcd = fs.put(obj['org_zip'])
        ogj['org_zip']=bcd
    ogj['img'] = li
    return ogj
def stlog1(log):
    # print('stlog1')
    with open('./log/loglisi1.log','w',encoding='utf8') as f:
        f.write(str(log))
    # print('elog1')
def stlog2(log):
    # print('stlog2')
    with open('./log/loglisi2.log','w',encoding='utf8') as f:
        f.write(str(log))
    # print('elog2')
log2d=[]
tttm=time.time()
logn=str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))+'-'
def donlog2(log):
    # print('stdlog2')
    global tttm
    global log2d
    ti1me='['+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+']'
    logg=ti1me+log
    log2d.append(logg)
    if len(log2d) >1000 or time.time()-tttm>500:
        stg=''
        for i in log2d:
            stg=stg+i+'\n'

        with open('./log/'+logn+'logdon.log','a',encoding='utf8') as f:
            f.write(str(stg))
        tttm = time.time()
        log2d = []
    # print('edlog2')


log2d1 = []
tttm1 = time.time()


def wlog2(log):
    # print('stdlog2')
    global tttm1
    global log2d1
    ti1me = '[' + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ']'
    logg = ti1me + log
    log2d.append(logg)
    if len(log2d) > 1000 or time.time() - tttm1 > 500:
        stg = ''
        for i in log2d:
            stg = stg + i + '\n'

        with open('./log/'+logn+'logw.log', 'a', encoding='utf8') as f:
            f.write(str(stg))
        tttm1 = time.time()
        log2d1 = []
def statrloop(F2TMq: queue.Queue, TM2DTq: queue.Queue, DT2TMq: queue.Queue, TM2Tq: queue.Queue, T2TMq: queue.Queue,q_log: queue.Queue,
            task_mask=10):
    t1=threading.Thread(target=TM_loop, args=(F2TMq, TM2DTq, DT2TMq, TM2Tq, T2TMq,q_log,task_mask))
    t1.start()
    t2 = threading.Thread(target=Tpool_loop_gid, args=( TM2DTq, DT2TMq, q_log, ))
    t2.start()
    t3 = threading.Thread(target=Tpool_loop_d, args=(TM2Tq, T2TMq, q_log, DT2TMq))
    t3.start()


def TM_loop(F2TMq: queue.Queue, TM2DTq: queue.Queue, DT2TMq: queue.Queue, TM2Tq: queue.Queue, T2TMq: queue.Queue,q_log: queue.Queue,
            task_mask=10):
    li = []
    TImects = time.time()
    # global TImects
    cwt=0
    Tmc=0
    while True:
        if time.time() -TImects>3600:
            TImects=time.time()
            cwt=1
            Tmc=time.time()
            print('1h s')

        if time.time() -Tmc>60 and cwt==1:
            cwt = 0


            print('1h dendaiend')



        ltl = len(li)
        if cwt==0:
            if ltl < task_mask:
                try:
                    tast = ist.get_wait_id()
                except Exception:
                    tast = None
                if str(tast) in li:
                    tast = None

                if tast is not None:
                    li.append(str(tast))
                    stlog1(li)
                    donlog2('addid '+str(tast))
                    TM2Tq.put(tast)

        if not F2TMq.empty():
            td=F2TMq.get()
            if td['type']=='id':
                if not ist.cheak_is_in(td['item']['id']):
                    # ist.write_id(t['id'], basep, t['y'])
                    ist.write_id(td['item']['id'], basep, 1)
            else:
                TM2DTq.put(td)


        if not DT2TMq.empty():
            for _ in range(10):
                if DT2TMq.empty():
                    break
                t=DT2TMq.get()
                if not ist.cheak_is_in(str(t['id'])) and not str(t['id']) in li:
                    wlog2('addid '+str(t['id']))
                    ist.write_id(t['id'], basep, t['y'])


        if not T2TMq.empty():
            fin: dict = T2TMq.get()



            # {'err':(t/f),'id':,'item':{}} {'p_id':pid,'img':img,'type':type,'intruduct':intruduct,'tag':tag,'tag_fy':tag_fy,'author':author

            # ,'title':title,'age':age
            # ,'add_time':add_time,
            #  'farm_time':farm_time,'org_zip':org_zip,'context':context

            #  }
            if fin['err'] == 'T':
                li.remove(fin['id'])
                if fin.get('idx') is not None:
                    ist.write_id(fin['id'], basep, 0)
                else:

                    ist.write_id(fin['id'], basep, 1)
            else:
                li.remove(fin['id'])
                donlog2('done ' + str(fin['id']))
                stlog2(li)
                items=fin['item']
                ii=0
                while ii<10:
                    try:
                        a=cfgg.db[cfgg.db_name]['pixiv']
                        a.insert_one(cad(items))
                        break
                    except Exception as e:
                        print(e)
                        print('dbeeeeee')
                        ii+=1
                if ii==10:
                    ist.write_id(fin['id'], basep, 1)
                else:
                    ist.write_id_arie(fin['id'],3,'./data/t/')
        if not q_log.empty():
            fin12= q_log.get()
            print('[' + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ']',str(fin12))


def T_pack_gid(p, l, q: queue.Queue,q1,q2):
    try:
        # h(l)
        time.sleep(1 + random.randint(1, 2) + random.random())
        run_Gid(cookies=cfgg.cookie,proxies=cfgg.proxy,headers=cfgg.headers,items=l,q_log=q,q_out=q1,q_out2self=q2)
    except Exception as ex:
        # print("Exception",ex)
        q.put({'err': ex})


    finally:
        p.putp()


def Tpool_loop_gid(TM2DTq: queue.Queue, DT2TMq: queue.Queue, ERR_back_Q: queue.Queue, pool_size: int = 3):
    pool = T_pool.T_pool(pool_size)
    # {'pid':111,}

    while True:
        tast = TM2DTq.get()

        t = pool.gett()
        t1 = t(target=T_pack_gid, args=(pool, tast, ERR_back_Q,DT2TMq,TM2DTq))
        t1.start()

def T_pack_d(p, l, q: queue.Queue,q1,DT2TMq2):
    try:
        # h(l)
        # run_Gid(cookies=cfgg.cookie,proxies=cfgg.proxies,headers=cfgg.headers,items=l,q_log=q,q_out=q1,q_out2self=q2)
        time.sleep(1+random.randint(1,4)+random.random())
        a=done(id=l,Q_log=q,Q_out=q1,cookies=cfgg.cookie,proxies=cfgg.proxy,headers=cfgg.headers,qs=DT2TMq2)
        a.run()
        # a.join()
    except Exception as ex:
        # print("Exception",ex)
        q.put({'err': ex})
        q.put('{未知错误}')
        q1.put({'err': 'T', 'id': str(l),'idx':0})
        with open ('logeee','a',encoding='utf-8') as f:
            f.write(str(ex))
            f.write('    ')
            f.write(l)
            f.write('\n')


    finally:
        p.putp()


def Tpool_loop_d(TM2Tq: queue.Queue, DT2TMq: queue.Queue, ERR_back_Q: queue.Queue,DT2TMq2, pool_size: int = 6):
    pool = T_pool.T_pool(pool_size)
    # {'pid':111,}

    while True:
        tast = TM2Tq.get()

        t = pool.gett()
        t1 = t(target=T_pack_d, args=(pool, tast, ERR_back_Q,DT2TMq,DT2TMq2))
        t1.start()
