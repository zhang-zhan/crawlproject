__author__ = 'zhangzhan1'
# -*- coding: utf-8 -*-
import codecs
from threading import Lock
#from UidUsedlog import *
#from getUseduid import *
import Queue

mutex = Lock()
UidQueue = Queue.Queue(maxsize=1100000)

def uidToQueue(nump):   #把UID读入到队列中
    global UidQueue
    '''with codecs.open('AllUid.txt',encoding='utf-8') as fp:
        for uid in fp:
            useruid = uid.strip('\t\r\n')
            UidQueue.put(useruid)'''
    fp = codecs.open("uid/AllUid.txt","r")
    lines = fp.readlines()
    fp.close()
    length = len(lines)
    for i in range(nump,length):
        line = lines[i].strip("\r\t\n")
        UidQueue.put(line)

def getNextUid(judge):#返回UID列表
    with mutex:
        global UidQueue
        uidlist = []
        number = 400    #返回给客户端的UID个数
        cursor = 0
        if judge == -1: #机器重新运行，根据已下载的个数，把未下载的UID读入队列
            uidcount = getNumUid()
            uidToQueue(uidcount)
            if UidQueue.empty():    #判断uid是否已用完
                clearUidUsedLog()
                uidToQueue(0)
                while cursor < number:
                    if UidQueue.empty():
			clearUidUsedLog()
			uidToQueue(0)
                        return uidlist, True
                    else:
                        uid = UidQueue.get()
                        uidlist.append(uid)
                        sUid(uid)
                    cursor += 1
            else:
                while cursor < number:
                    if UidQueue.empty():
			clearUidUsedLog()
			uidToQueue(0)
                        return uidlist, True
                    else:
                        uid = UidQueue.get()
                        uidlist.append(uid)
                        sUid(uid)
                    cursor += 1
        elif judge == 0:
            if UidQueue.empty():
                clearUidUsedLog()
		uidToQueue(0)
                return uidlist, True
            else:
                while cursor < number:
                    if UidQueue.empty():
			clearUidUsedLog()
			uidToQueue(0)
                        return uidlist, True
                    else:
                        uid = UidQueue.get()
                        uidlist.append(uid)
                        sUid(uid)
                    cursor += 1
        return uidlist, False

def getNumUid():#获取已下载的UID个数
    fp1 = codecs.open("logInfo/UidUsedlog.txt","r")
    lines = fp1.readlines()
    fp1.close()
    uidnum = len(lines)
    return uidnum

def putUidToQue(UID): #把出错的UID重新下载
    global UidQueue
    UidQueue.put(UID)

def deleteUid(uid):#删除用户不存在的UID
    uid = str(uid)
    fp2= codecs.open("uid/AllUid.txt")
    f=fp2.readlines()
    fp2.close()
    index = f.index(uid+"\n")
    del f[index]
    w = codecs.open("uid/AllUid.txt","w")
    w.write("".join(f))
    w.close()

def sUid(uid):#把已用的UID存入文件中
    fp3 = codecs.open("logInfo/UidUsedlog.txt","a")
    fp3.write(uid+"\n")
    fp3.close()

def clearUidUsedLog():#清空已用UID
    uf = codecs.open("logInfo/UidUsedlog.txt","rb+")
    uf.truncate()
    uf.close()

def sUid(uid):
 fp4 = codecs.open("logInfo/UidUsedlog.txt","a")
 fp4.write(uid+"\n")
 fp4.close()

''' def rewind(self,number):
        with mutex:
            global fp
            global cursor
            if number==0:
                return
            elif number > 0:
                i = 0
                for line in fp:
                    i += 0
                    if i>=number:
                        break
            else:
                c = cursor + number
                open_uid_file()
                i = 0
                for line in fp:
                    i += 0
                    if i>=number:
                        break



            cursor = 0
            data = list()
            c = 0
            n = openfile()
            if n == "no":
                return "no"
            for line in fp:
                line = line.strip(' \t\r\n')
                if judge == -1:
                   c += 1
                   if n>=c:
                      continue
                   else:
                      cursor += 1

                      data.append(line)
                      s = Saveuid()
                      s.saveuid(line)
                      if cursor >= number:
                        break
                else:
                  cursor += 1

                  data.append(line)
                  s = Saveuid()
                  s.saveuid(line)
                  if cursor >= number:
                      break
        return data'''

'''data = open(filename, 'rt').readlines()
with open(filename, 'wt') as handle:
    handle.writelines(data[:tobedeleted])
    handle.writelines(data[tobedeleted+1:])'''
