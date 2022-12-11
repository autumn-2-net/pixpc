import lzma
import pprint
import queue
import io
import threading
import zipfile

import httpx
import imageio
from lib.inst_tool import cheak_is_in
from lib.DB_uase import prp_data as prp_datas
headers = {
    "Host": "www.pixiv.net",
    "referer": "https://www.pixiv.net/",
    "origin": "https://accounts.pixiv.net",
    "accept-language": "zh-CN,zh;q=0.9",
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}


def set_cookie_a(cookie: str):
    cookies1 = httpx.Cookies()
    c_list = cookie.split(';')
    for c in c_list:
        # print(c)
        ds = c.split('=', maxsplit=1)
        # print(ds)
        cookies1.set(ds[0].strip(), ds[1].strip())
    return cookies1


def R_get(cookies, url, params, headers=None):
    i = 0
    if headers is None:
        headers = headers
    while i < 10:
        try:
            response = httpx.get(
                url,

                params=params,
                cookies=cookies,
                headers=headers,
                verify=False,
                timeout=10,
            )
            return {'err': 0, 're': response}
        except httpx.HTTPError:
            i = i + 1
    return {'err': 1, }


def R_get_np(cookies, url, headers=None):
    i = 0
    if headers is None:
        headers = headers
    while i < 10:
        try:
            response = httpx.get(
                url,

                cookies=cookies,
                headers=headers,
                verify=False,
                timeout=10,
            )
            return {'err': 0, 're': response}
        except httpx.HTTPError:
            i = i + 1
    return {'err': 1, }





class done:
    def __init__(self, id, headers, cookies, proxies, Q_out: queue.Queue, Q_log: queue.Queue,qs: queue.Queue):


        self.id = id
        # self.type = type
        self.Q_out: queue.Queue = Q_out
        self.Q_log: queue.Queue = Q_log
        self.headers = headers
        self.cookies = cookies
        self.proxies = proxies
        self.artworks_url = "https://www.pixiv.net/artworks/{}"
        # 作品数据
        self.ajax_illust = "https://www.pixiv.net/ajax/illust/{}"
        # 动图的zip包下载地址
        self.zip_url = "https://www.pixiv.net/ajax/illust/{}/ugoira_meta"
        # 多图-每张图的url组
        self.multi_url = "https://www.pixiv.net/ajax/illust/{}/pages"
        self.qs=qs

    def httpgat(self, link1, cookies2=None, header=None, proxies=None):
        if cookies2 is None:
            cookies2 = self.cookies
        if header is None:
            header = self.headers
        if proxies is None:
            proxies = self.proxies

        i = 0
        while i < 15:
            try:
                c = httpx.get(link1, cookies=cookies2, headers=header, proxies=proxies)
                return {'err': 'F', 'item': c}
            except Exception:
                i = i + 1

        self.Q_log.put(str(self.id)+'http错误')
        return {'err': 'T'}

    def run(self):
        # print( "Running")
        arcl = self.ajax_illust.replace('{}', str(self.id))  # {'err':(t/f),'id':,'item':{}}
        ctr = self.httpgat(arcl)
        # print(ctr)
        if ctr['err'] == 'T':
            self.Q_log.put(str(self.id)+'http错误')
            self.Q_out.put({'err': 'T', 'id': self.id})
            return 0
        try:
            ctrj = ctr['item'].json()
        except:
            self.Q_log.put(str(self.id)+'解析错误')
            self.Q_out.put({'err': 'T', 'id': self.id})
            return 0
        if ctrj['error']:
            self.Q_log.put(str(self.id)+'服务端错误')
            self.Q_out.put({'err': 'T', 'id': self.id,'item':{}})
            return 0

        # pprint.pprint(ctrj) #######################################################################
        inff = self.getinfo(ctrj)
        # pprint.pprint(inff)

        # print(inff['typess'])
        if inff['typess'] == 's':
            self.simdd(inff, ctrj)
        if inff['typess'] == 'd':
            self.muimgd(inff, ctrj)
        if inff['typess'] == 'g':
            self.gifdd(inff, ctrj)
        if inff['typess'] == 'ms':
            self.ms_d(inff, ctrj)
        # self.gifdd(inff,ctrj)
        if inff['typess'] == 'md':
            self.md_d(inff, ctrj)

    def ms_d(self, info, j):  #####################################################################
        contc = j['body']['seriesNavData']
        if contc is None:
            nextc = 'none'
            prevc = 'none'
        else:
            if contc['next'] is None:
                nextc = 'none'
            else:
                nextc = contc['next']['id']
            if contc['prev'] is None:
                prevc = 'none'
            else:
                prevc = contc['prev']['id']
        c = j['body']['urls']['original']
        img = self.s_img_get(c)
        if img is None:
            # 错误处理
            return None
        img = lzma.compress(img, preset=6)
        # {'title':title,'illustComment':illustComment,'uid':uid,'userName':userName,'tag':tag,'tag_fy':tag_fy,'age':age,'typess':typess,'Ttype':Ttype}
        dbl = prp_datas(pid=self.id, img=[img], intruduct=info['illustComment'], age=info['age'],
                        author={info['uid']: info['userName']}, tag=info['tag'],
                        tag_fy=info['tag_fy'], title=info['title'], types=info['Ttype'], context=[nextc, prevc])
        self.Q_out.put({'err': 'F', 'id': self.id, 'item': dbl})
        if nextc!='none':
            self.qs.put({'id': nextc, 'y': 3})
        if prevc!='none':
            self.qs.put({'id': prevc, 'y': 3})



    # print(dbl)

    def md_d(self, info, j):
        contc = j['body']['seriesNavData']
        if contc is None:
            nextc = 'none'
            prevc = 'none'
        else:
            if contc['next'] is None:
                nextc = 'none'
            else:
                nextc = contc['next']['id']
            if contc['prev'] is None:
                prevc = 'none'
            else:
                prevc = contc['prev']['id']
        midl = self.multi_url.replace('{}', str(self.id))
        ctr = self.httpgat(midl)
        # print(ctr)
        if ctr['err'] == 'T':
            self.Q_log.put(str(self.id)+'解析错误md')
            self.Q_out.put({'err': 'T', 'id': self.id})
            return 0
        try:
            ctrj = ctr['item'].json()
        except:
            self.Q_log.put(str(self.id)+'解析错误md')
            self.Q_out.put({'err': 'T', 'id': self.id})
            return 0
        if ctrj['error']:
            self.Q_log.put(str(self.id)+'服务端错误md')
            self.Q_out.put({'err': 'T', 'id': self.id})
            return 0
        # pprint.pprint(ctrj)
        lsit = []
        for i in ctrj['body']:
            utli = i['urls']['original']
            img = self.s_img_get(utli)
            if img is None:
                # 错误处理
                return None

            lsit.append(lzma.compress(img, preset=6))  # 压缩文件
        dbl = prp_datas(pid=self.id, img=lsit, intruduct=info['illustComment'], age=info['age'],
                        author={info['uid']: info['userName']}, tag=info['tag'],
                        tag_fy=info['tag_fy'], title=info['title'], types=info['Ttype'], context=[nextc, prevc])
        self.Q_out.put({'err': 'F', 'id': self.id, 'item': dbl})
        if nextc != 'none':
            self.qs.put({'id': nextc, 'y': 3})
        if prevc != 'none':
            self.qs.put({'id': prevc, 'y': 3})

    # print(dbl)
    def gifdd(self, info, j):
        glink = self.zip_url.replace('{}', str(self.id))
        ctr = self.httpgat(glink)
        # print(ctr)
        if ctr['err'] == 'T':
            self.Q_log.put(str(self.id)+'解析错误gif')
            self.Q_out.put({'err': 'T', 'id': self.id})
            return 0
        try:
            ctrj = ctr['item'].json()
        except:
            self.Q_log.put(str(self.id)+'解析错误gif')
            self.Q_out.put({'err': 'T', 'id': self.id})
            return 0
        if ctrj['error']:
            self.Q_log.put(str(self.id)+'服务端错误gif')
            self.Q_out.put({'err': 'T', 'id': self.id})
            return 0
        # pprint.pprint(ctrj)
        ziplink = ctrj['body']['originalSrc']
        frml = ctrj['body']['frames']
        zipp = self.httpgat(ziplink)
        # print(ctr)
        if zipp['err'] == 'T':
            self.Q_log.put({})
            self.Q_out.put({'err': 'T', 'id': self.id})
            return 0
        itemm = zipp['item'].content
        zipf = io.BytesIO(itemm)
        with zipfile.ZipFile(zipf, "r") as f2:
            # print(f2.namelist())
            l = []
            p = []
            for file in frml:
                l.append(imageio.imread(io.BytesIO(f2.read(file['file']))))
                p.append(file['delay'] / 1000)
            # print(file)
        ccc = imageio.mimsave('<bytes>', l, format='GIF', duration=p)
        # with open('test.gif', 'wb') as f:
        #     f.write(ccc)
        img = lzma.compress(ccc, preset=6)
        dbl = prp_datas(pid=self.id, img=[img], intruduct=info['illustComment'], age=info['age'],
                        author={info['uid']: info['userName']}, tag=info['tag'],
                        tag_fy=info['tag_fy'], title=info['title'], types=info['Ttype'], farm_time=frml,
                        org_zip=lzma.compress(itemm, preset=6))
        self.Q_log.put(str(self.id)+'{g下载完成}')
        self.Q_out.put({'err': 'F', 'id': self.id, 'item': dbl})

    # print(dbl)

    def get_type(self, pageCount, illustType):
        '''======以下为判定规则========
						  单图 多图 动图 漫画单图 漫画多图
				pageCount  1	 n 	  1    1      n
				illustType 0	 0 	  2    1	  1
				==========================='''
        if pageCount == 1 and illustType == 0:
            return 's'  # 单图
        if pageCount > 1 and illustType == 0:
            return 'd'  # 多图
        if pageCount == 1 and illustType == 2:
            return 'g'  # 动图
        if pageCount == 1 and illustType == 1:
            return 'ms'  # 漫画单图 seriesNavData
        if pageCount > 1 and illustType == 1:
            return 'md'  # 漫画多图

    def get_T_type(self, item):
        if item in ['s', 'd']:
            return 'img'  # 普通图片
        if item in ['ms', 'md']:
            return 'mg'  # 漫画
        if item in ['g']:
            return 'g'

    def s_img_get(self, li):
        c = self.httpgat(li)
        if c['err'] == 'F':  # {'err':'F','item':c}
            if len(c['item'].content)<900:
                self.Q_log.put('{图片太小哦啊}')
                self.Q_out.put({'err': 'T', 'id': self.id,'idx':0})
                return None
            return c['item'].content
        else:
            return None

    def simdd(self, info, j, ):
        c = j['body']['urls']['original']
        img = self.s_img_get(c)
        if img is None:
            # 错误处理
            return None
        img = lzma.compress(img, preset=6)
        # {'title':title,'illustComment':illustComment,'uid':uid,'userName':userName,'tag':tag,'tag_fy':tag_fy,'age':age,'typess':typess,'Ttype':Ttype}
        dbl = prp_datas(pid=self.id, img=[img], intruduct=info['illustComment'], age=info['age'],
                        author={info['uid']: info['userName']}, tag=info['tag'],
                        tag_fy=info['tag_fy'], title=info['title'], types=info['Ttype'], )
        self.Q_out.put({'err': 'F', 'id': self.id, 'item': dbl})

    # print(dbl)
    def muimgd(self, info, j, ):
        midl = self.multi_url.replace('{}', str(self.id))
        ctr = self.httpgat(midl)
        # print(ctr)
        if ctr['err'] == 'T':
            self.Q_log.put({})
            self.Q_out.put({'err': 'T', 'id': self.id})
            return 0
        try:
            ctrj = ctr['item'].json()
        except:
            self.Q_log.put({})
            self.Q_out.put({'err': 'T', 'id': self.id})
            return 0
        if ctrj['error']:
            self.Q_log.put({})
            self.Q_out.put({'err': 'T', 'id': self.id})
            return 0
        # pprint.pprint(ctrj)
        lsit = []
        for i in ctrj['body']:
            utli = i['urls']['original']
            img = self.s_img_get(utli)
            if img is None:
                # 错误处理
                return None

            lsit.append(lzma.compress(img, preset=6))  # 压缩文件
        dbl = prp_datas(pid=self.id, img=lsit, intruduct=info['illustComment'], age=info['age'],
                        author={info['uid']: info['userName']}, tag=info['tag'],
                        tag_fy=info['tag_fy'], title=info['title'], types=info['Ttype'], )
        self.Q_out.put({'err': 'F', 'id': self.id, 'item': dbl})

    def getinfo(self, j):

        bd = j['body']

        title = bd['illustTitle']
        illustComment = bd['illustComment']
        tggg = bd['tags']['tags']
        # 作品类型
        illustType = bd["illustType"]
        # 页数
        pageCount = bd["pageCount"]
        uid = int(bd["userId"])
        # userName
        userName = bd["userName"]
        tag = []
        tag_fy = []
        age = 'n'  # n r rg
        for i in tggg:
            tag.append(i['tag'])
            fy = i.get('translation')
            if fy is None:
                fy = i['tag']

            else:
                fy = fy.get('en')

            tag_fy.append({i['tag']: fy})
        if tag[0] == 'R-18G':
            age = 'rg'
        if tag[0] == 'R-18':
            age = 'r'

        typess = self.get_type(pageCount=pageCount, illustType=illustType)
        Ttype = self.get_T_type(typess)

        return {'title': title, 'illustComment': illustComment, 'uid': uid, 'userName': userName, 'tag': tag,
                'tag_fy': tag_fy, 'age': age, 'typess': typess, 'Ttype': Ttype}


class id_G:
    def __init__(self, types, item, headers, cookies, proxies,
                 Q_log: queue.Queue,qtm: queue.Queue,qdt: queue.Queue ):  # type 有 bm bmf authon tag tagf  s_tc   att
        self.headers = headers
        self.cookies = cookies
        self.proxies = proxies
        self.Q_log = Q_log
        self.types = types
        self.item = item
        self.qdt=qdt
        self.qt=qtm

    def run(self):
        # print('rrrr')
        if self.types == 'authon':
            self.authon()
        if self.types in ['tag', 'tagf', 's_tc']:
            self.tag()
        if self.types == 'bmf':
            self.bmf()
        if self.types == 'bm':
            self.bm()
        if self.types == 'att':
            self.att()

    def att(self):
        # {uid}
        uid = self.item['uid']
        base = 'https://www.pixiv.net/ajax/user/{u}/following?offset={off}&limit=24&rest=show&tag=&acceptingRequests=0&lang=zh'.replace(
            '{u}', str(uid))
        lo = []
        ioi = 1
        while True:
            link = base.replace('{off}', str((ioi - 1) * 24))
            ioi = ioi + 1
            # print(link)
            ctr = self.httpgat(link)
            # print(link)
            # print(ctr)
            if ctr['err'] == 'T':
                self.Q_log.put({})
                # self.Q_out.put({'err': 'T', 'id': self.id})
                return None
            try:
                ctrj = ctr['item'].json()
            except:
                self.Q_log.put({})
                # self.Q_out.put({'err': 'T', 'id': self.id})
                return None
            if ctrj['error']:
                self.Q_log.put({})
                # self.Q_out.put({'err': 'T', 'id': self.id})
                return None
            if ctrj['body']['users'] == []:
                break
            for i in ctrj['body']['users']:
                # print(i)

                id = i['userId']

                # lo.append({'type': 'authon', 'item': {'aid': id}})
                self.qdt.put({'type': 'authon', 'item': {'aid': id}})

        # print(lo)
        # return lo

    def page(self, p):
        return (p - 1) * 48

    def bm(self):
        # {uid,}
        uid = self.item['uid']
        bas = 'https://www.pixiv.net/ajax/user/{uid}/illusts/bookmarks?tag=&offset={off}&limit=48&rest=show&lang=zh'.replace(
            '{uid}', str(uid))
        bash = 'https://www.pixiv.net/ajax/user/{uid}/illusts/bookmarks?tag=&offset={off}&limit=48&rest=hide&lang=zh'.replace(
            '{uid}', str(uid))
        lo = []
        ioi = 1
        while True:
            link = bash.replace('{off}', str(self.page(ioi)))
            ioi = ioi + 1
            ctr = self.httpgat(link)
            # print(link)
            # print(ctr)
            if ctr['err'] == 'T':
                self.Q_log.put({})
                # self.Q_out.put({'err': 'T', 'id': self.id})
                return None
            try:
                ctrj = ctr['item'].json()
            except:
                self.Q_log.put({})
                # self.Q_out.put({'err': 'T', 'id': self.id})
                return None
            if ctrj['error']:
                self.Q_log.put({})
                # self.Q_out.put({'err': 'T', 'id': self.id})
                return None
            if ctrj['body']['works'] == []:
                break
            iop = 0
            for i in ctrj['body']['works']:
                # print(i)
                if i['isMasked']:
                    continue
                ag = i['tags']
                id = i['id']
                if cheak_is_in(id):  #####################################################
                    iop = 1
                    break
                yy = 3
                if ag[0] == 'R-18G':
                    yy = 1
                if ag[0] == 'R-18':
                    yy = 2
                # lo.append({'id': id, 'y': yy})
                self.qt.put({'id': id, 'y': yy})
            if iop == 1:
                break
        while True:
            link = bas.replace('{off}', str(self.page(ioi)))
            ioi = ioi + 1
            ctr = self.httpgat(link)
            # print(link)
            # print(ctr)
            if ctr['err'] == 'T':
                self.Q_log.put({})
                # self.Q_out.put({'err': 'T', 'id': self.id})
                return None
            try:
                ctrj = ctr['item'].json()
            except:
                self.Q_log.put({})
                # self.Q_out.put({'err': 'T', 'id': self.id})
                return None
            if ctrj['error']:
                self.Q_log.put({})
                # self.Q_out.put({'err': 'T', 'id': self.id})
                return None
            if ctrj['body']['works'] == []:
                break
            iop = 0
            for i in ctrj['body']['works']:
                # print(i)
                if i['isMasked']:
                    continue
                ag = i['tags']
                id = i['id']
                if cheak_is_in(id):  #####################################################
                    iop = 1
                    break
                yy = 3
                if ag[0] == 'R-18G':
                    yy = 1
                if ag[0] == 'R-18':
                    yy = 2
                self.qt.put({'id': id, 'y': yy})
            if iop == 1:
                break
        # return lo

    def bmf(self):
        # {uid,}
        uid = self.item['uid']
        bas = 'https://www.pixiv.net/ajax/user/{uid}/illusts/bookmarks?tag=&offset={off}&limit=48&rest=show&lang=zh'.replace(
            '{uid}', str(uid))
        bash = 'https://www.pixiv.net/ajax/user/{uid}/illusts/bookmarks?tag=&offset={off}&limit=48&rest=hide&lang=zh'.replace(
            '{uid}', str(uid))
        lo = []
        ioi = 1
        while True:
            link = bash.replace('{off}', str(self.page(ioi)))
            ioi = ioi + 1
            ctr = self.httpgat(link)
            # print(link)
            # print(ctr)
            if ctr['err'] == 'T':
                self.Q_log.put({})
                # self.Q_out.put({'err': 'T', 'id': self.id})
                return None
            try:
                ctrj = ctr['item'].json()
            except:
                self.Q_log.put({})
                # self.Q_out.put({'err': 'T', 'id': self.id})
                return None
            if ctrj['error']:
                self.Q_log.put({})
                # self.Q_out.put({'err': 'T', 'id': self.id})
                return None
            if ctrj['body']['works'] == []:
                break
            for i in ctrj['body']['works']:
                # print(i)
                if i['isMasked']:
                    continue
                ag = i['tags']
                id = i['id']
                yy = 3
                if ag[0] == 'R-18G':
                    yy = 1
                if ag[0] == 'R-18':
                    yy = 2
                print('add',str(id))
                self.qt.put({'id': id, 'y': yy})
        while True:
            link = bas.replace('{off}', str(self.page(ioi)))
            ioi = ioi + 1
            ctr = self.httpgat(link)
            # print(link)
            # print(ctr)
            if ctr['err'] == 'T':
                self.Q_log.put({})
                # self.Q_out.put({'err': 'T', 'id': self.id})
                return None
            try:
                ctrj = ctr['item'].json()
            except:
                self.Q_log.put({})
                # self.Q_out.put({'err': 'T', 'id': self.id})
                return None
            if ctrj['error']:
                self.Q_log.put({})
                # self.Q_out.put({'err': 'T', 'id': self.id})
                return None
            if ctrj['body']['works'] == []:
                break
            for i in ctrj['body']['works']:
                # print(i)
                if i['isMasked']:
                    continue
                ag = i['tags']
                id = i['id']
                yy = 3
                if ag[0] == 'R-18G':
                    yy = 1
                if ag[0] == 'R-18':
                    yy = 2
                self.qt.put({'id': id, 'y': yy})
        # return lo

    def httpgat(self, link1, cookies2=None, header=None, proxies=None):
        if cookies2 is None:
            cookies2 = self.cookies
        if header is None:
            header = self.headers
        if proxies is None:
            proxies = self.proxies

        i = 0
        while i < 15:
            try:
                c = httpx.get(link1, cookies=cookies2, headers=header, proxies=proxies)
                return {'err': 'F', 'item': c}
            except Exception:
                i = i + 1

        self.Q_log.put({})
        return {'err': 'T'}

    def authon(self):
        aid = self.item['aid']
        basl = 'https://www.pixiv.net/ajax/user/{uid}/profile/all?lang=zh'.replace('{uid}', str(aid))
        ctr = self.httpgat(basl)
        # print(ctr)
        if ctr['err'] == 'T':
            self.Q_log.put({})
            # self.Q_out.put({'err': 'T', 'id': self.id})
            return None
        try:
            ctrj = ctr['item'].json()
        except:
            self.Q_log.put({})
            # self.Q_out.put({'err': 'T', 'id': self.id})
            return None
        if ctrj['error']:
            self.Q_log.put({})
            # self.Q_out.put({'err': 'T', 'id': self.id})
            return None
        bdi = ctrj['body']['illusts']
        # print(bdi)
        lo = []
        for i in bdi:
            # print(i)
            if i is None:
                continue
            self.qt.put({'id': i, 'y': 2})
        # return lo

    def tag(self):
        # {word,md}
        # md 有all he r18  sm 有 s_tag 和 s_tag_full s_tc 这个好像是一般的搜索
        tmp = 'https://www.pixiv.net/ajax/search/artworks/{worsd}?word={worsd}&order=date_d&mode={md}&p={page}&s_mode={sm}&type=all&lang=zh'
        tmp = tmp.replace('{md}', self.item['md']).replace('{worsd}', self.item['word'])
        if self.types == 'tag':
            tmp = tmp.replace('{sm}', 's_tag')
        if self.types == 'tagf':
            tmp = tmp.replace('{sm}', 's_tag_full')
        if self.types == 's_tc':
            tmp = tmp.replace('{sm}', 's_tc')
        ii = 1
        lo = []
        while True:
            # print(ii)
            link = tmp.replace('{page}', str(ii))
            ctr = self.httpgat(link)
            # print(ctr)
            if ctr['err'] == 'T':
                self.Q_log.put({})
                # self.Q_out.put({'err': 'T', 'id': self.id})
                return None
            try:
                ctrj = ctr['item'].json()
            except:
                self.Q_log.put({})
                # self.Q_out.put({'err': 'T', 'id': self.id})
                return None
            if ctrj['error']:
                self.Q_log.put({})
                # self.Q_out.put({'err': 'T', 'id': self.id})
                return None
            # illustManga
            # data
            if ctrj['body']['illustManga']['data'] == []:
                break
            for i in ctrj['body']['illustManga']['data']:
                ag = i['tags']
                id = i['id']
                yy = 3
                if ag[0] == 'R-18G':
                    yy = 1
                if ag[0] == 'R-18':
                    yy = 2
                self.qt.put({'id': id, 'y': yy})
            ii = ii + 1
        # return lo

#{'type': 'authon', 'item': {'aid': id}}
def run_Gid(items,q_out2self:queue.Queue,q_out:queue.Queue,q_log:queue.Queue, headers, cookies, proxies):

    if items['type']=='att':
        idgg = id_G(items['type'],items['item'],headers, cookies, proxies,q_log,qdt=q_out2self,qtm=q_out)
        idgg.run()


    else:
        idgg = id_G(items['type'],items['item'],headers, cookies, proxies,q_log,qdt=q_out2self,qtm=q_out)
        idgg.run()



