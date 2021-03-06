__author__ = 'zhangzhan1'
# -*- coding: UTF-8 -*-
import web
import codecs
import urlparse
import json
import xmlrpclib
from threading import Lock
from GetUid import  *
from GetLink import baseclass
from uidlog import *
from threading import Lock
#from sql import *
from rToken import *
from getUseduid import *
import time
import datetime
import threading

import judgeThread

"""
需要配置的数据
"""
ClientNUM = 15
remainNUM = 5 #剩余数小于此值时，启动判断线程
hostIP = [""]

"""
END
"""
errUidList = [] #存储出错的UID
runJudge = -1 #用来判断机器是否重新运行
#count = -1
tokens = []
data = {}
host = {} #主机上次的申请的时间

lastRTime = {} #客户端上次更新时间
MaxInterVal = 0 #最大时间间隔
allFinished = False
notJudgeRun = True
t_Mutex = threading.Lock()

expiredlist_token = []
tokenexpired = []
ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'
finished = 0
render = web.template.render('templates')

urls = (
    '/hostname=(.*)', 'pull',
    '/index', 'index',
    '/request', 'request',
    '/click', 'click',
    '/rec_uid', 'rec_uid',
    '/rec_uid_access', 'rec_uid_access',
    '/rec_uid_nexist', 'rec_uid_nexist',
    '/rec_uid_other', 'rec_uid_other',
    '/userFill','userFill',
    '/user','user',
    "/recToken","recToken", # 接受token
)
rLock = Lock()
class recToken:
    def POST(self):
        with rLock:
            i = web.data()
            i = json.loads(i)
            fr = open('./conInfo/accesstoken.txt',"r")
            tk = fr.readlines()
            fr.truncate()
            fr.close()
            fw = open("./conInfo/accesstoken.txt","a")
            tokenData = i["token"]
            hn = i["hostname"]

            for td in tokenData:
                fw.write(td+"\t"+hn+"\n")


            for line in tk:
                tkn,hne = line.strip().split("\t")
                if hne == hn:
                    continue
                else:
                    fw.write(tkn+"\t"+hne+"\n")


            fw.close()



# class userFill:
#     def GET(self):
#         return render.userFill()
#
# class user:
#     def POST(self):
#         ud = web.data()
#         for uid in ud:
#             try:
#                 if isinstance(uid,int):
#                     print uid
#                     uToQueue(uid)
#             except:
#                 continue




# class rec_uid_nexist:
#     def POST(self): #接受客户端发来的用户不存在的UID，并把它删除
#         i = web.data()
#         try:
#             i = json.loads(i)
#             uid = i['uid']
#             deleteUid(uid)     #删除UID
#         except ValueError:
#             print "cannot write"

# class rec_uid_other:
#     def POST(self):
#         global errUidList
#         i = web.data()
#         try:
#             i = json.loads(i)
#             uid = i['uid']
#             error = i['error']
#             if error == "User requests out of rate limit!":
#                 putUidToQue(uid)
#             if error == "IP requests out of rate limit!":
#                 putUidToQue(uid)
#             if uid not in errUidList:
#                 putUidToQue(uid)
#                 errUidList.append(uid)
#             u = Suid()
#             u.suid(uid,error,time,0)
#         except ValueError:
#            print "cannot write"

class rec_uid:
    def POST(self):
        # global errUidList
        # global tokenexpired
        i = web.data()
        try:
            i = json.loads(i)
            errorType = i['errorType']
            if errorType == 1:
                for ip in hostIP:
                    getToken(ip)
            #tokenexpired.append(token_expired)
            # if uid not in errUidList:
            #     putUidToQue(uid)
            #     errUidList.append(uid)
            # u = Suid()
            # u.suid(uid,error,time,0)
        except ValueError:
            print 'sending info'

# class rec_uid_access:
#     def POST(self):
#         global errUidList
#         global expiredlist_token
#         a = web.data()
#         try:
#             a = json.loads(a)
#             uid = a['uid']
#             access_token = a['access_token']
#             error = a['error']
#             time = a['time']
#             if uid not in errUidList:
#                 putUidToQue(uid)
#                 errUidList.append(uid)
#             u = Suid()
#             u.suid(uid,error,time,0)
#             expiredlist_token.append(access_token)
#         except ValueError:
#             print 'ERROR'

# class click:
#     def POST(self):
#
#         i = urlparse.parse_qs( web.data())
#         ip = str(i['IP'][0])
#         cmd = str(i['cmd'][0])
#         if cmd == "Start":
#            print 'the cmd is start'
#            start_spider(ip)
#            print "receive command"
#
#         else:
#             print 'the cmd is stop'
#             stop_spider(ip)


class pull:
    def GET(self, hostname):
        global finished     #uid下载完的标志
        global expiredlist_token
        global tokenexpired
        global runJudge
        global host
        global lastRTime
        global MaxInterVal
        global notJudgeRun
        global t_Mutex
        with rLock:
            hid = int(hostname) #主机ID
            print hid
            Host = str(hostname)
            print Host
            nt = int(time.mktime(time.strptime( time.strftime(ISOTIMEFORMAT), ISOTIMEFORMAT))) #获取当前时间

            if Host in lastRTime:
                mtmp = nt - lastRTime[Host]
                if(mtmp>MaxInterVal):
                    MaxInterVal = mtmp
            lastRTime[Host] = nt

            """获取UID""""""此处需要缓存队列"""
            #uids, finishJudge= getNextUid(runJudge)   #获取UID
            #runJudge = 0

            """此处需要缓存队列"""
            #if finishJudge == True:#用户UID下完的标志
                #finished = 1

            """启动判断线程"""
            if finished == 1 and (ClientNUM - len(host)) < remainNUM:
                if notJudgeRun:
                    t_Mutex.acquire()
                    if notJudgeRun:
                        th = threading.Thread(target=judgeThread.judgeThread)
                        th.start()
                        notJudgeRun = False
                    t_Mutex.release()


            if finished == 1:   #下完一遍，给每个客户端返回一个等待时间
                Time = time.strftime('%Y-%m-%d')
                nowtime  = int(time.mktime(time.strptime( time.strftime(ISOTIMEFORMAT), ISOTIMEFORMAT ) ))
                zerotime = int(time.mktime(time.strptime( Time+" 00:00:00", ISOTIMEFORMAT)))
                c = nowtime-zerotime
                host[Host] = nowtime
                sleeptime = 86400-c
                return sleeptime

            """获取UID""""""此处需要缓存队列"""
            uids, finishJudge= getNextUid(runJudge)   #获取UID
            runJudge = 0

            """此处需要缓存队列"""
            if finishJudge == True:#用户UID下完的标志
                finished = 1
            if uids == []:
                return None
            hId = hid-1
            token = rtoken(hId)   #获取token

            """此处token什么原因返回None，是没有可以的token，还是没有找到可以用的token"""
            '''while(True):
                if  token in expiredlist_token:
                      token = t.rtoken(hId)
                elif token in tokenexpired:
                    token = t.rtoken(hId)
                    if token in tokenexpired:
                        return None
                    else:
                        break
                else:
                      break'''

            b = baseclass('conInfo/config.txt')
            data = b.get_link(uids,token,0)

            return data

# class index:
#     def GET(self):
#         global data
#         nowtime = int(time.mktime(time.strptime( time.strftime(ISOTIMEFORMAT), ISOTIMEFORMAT)))
#         d = json.dumps(data,encoding='UTF-8')
#         return render.temp(d,nowtime)

# class request:
#     def POST(self):
#         global data
#         i = web.data()
#         try:
#             i = json.loads(i)
#             data[i['MAC']] = i
#             data[i['MAC']][u'receivetime'] = int(time.mktime(time.strptime( time.strftime(ISOTIMEFORMAT), ISOTIMEFORMAT ) ))
#         except ValueError:
#             print 'client is sending info'




def getToken(ip):
    url = "http://"+ip+":10090"
    server = xmlrpclib.ServerProxy(url,allow_none=True)
    server.run()
    print 'OK'


# def stop_spider(ip):
#     url = "http://"+ip+":10090"
#     server = xmlrpclib.ServerProxy(url,allow_none=True)
#     server.stop()
#     print 'OK'

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()


