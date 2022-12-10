from pymongo import MongoClient


class tcun:
    cookie =''
    uid=''
    maxT=''
    wait=''
    sc_time=''
    ly=3
    dbac=''
    db:MongoClient=''
    proxy=''
    db_name=''
    headers = {
    "Host": "www.pixiv.net",
    "referer": "https://www.pixiv.net/",
    "origin": "https://accounts.pixiv.net",
    "accept-language": "zh-CN,zh;q=0.9",
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}

cfgg=tcun()