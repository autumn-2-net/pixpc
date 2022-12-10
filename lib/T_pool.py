import queue
import threading
import time

# cff= queue.Queue(100)
# cff.put('dddddddddddddddddddddddddddddddddd')
# cff.put('dddddddddddddddddddddddddddddddddd')
# cff.put('dddddddddddddddddddddddddddddddddd')
# cff.put('dddddddddddddddddddddddddddddddddd')
# cff.put('dddddddddddddddddddddddddddddddddd')
# print(cff.get())
# print(cff.empty())
# print(cff.get())
# print(cff.get())
# print(cff.get())
# print(cff.get())
# print(cff.empty())
# print(cff.get())
class T_pool:
    def __init__(self,sx=20):
        self.q=queue.Queue(sx)
        for i in range(sx):
            self.q.put(threading.Thread)

    def gett(self):
        return self.q.get()
    def putp(self):
        self.q.put(threading.Thread)
    def empy(self):
        return self.q.empty()

def T_pack(p,h,l):
    try:
        h(l)
    except Exception as ex:
        print("Exception",ex)


    finally:
        p.putp()

def sss(l):
    print(l)
    raise 'sssss'

# d =T_pool(5)
# t =d.gett()
# t1=t(target=T_pack,args=(d,sss,'ll'))
# t1.start()
# for i in range(10):
#     t = d.gett()
#     t1 = t(target=T_pack, args=(d, sss, i))
#     t1.start()
#     print(d.empy())
# print(111111)
# del d
# time.sleep(1)







