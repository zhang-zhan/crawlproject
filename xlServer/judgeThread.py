#coding=utf-8
__author__ = 'jiaodongdong'
import datetime
import time
import xlServerCopy

def judgeThread():
    sval = int(xlServerCopy.MaxInterVal/10)
    isEnd = True
    while True:
        isEnd = True
        time.sleep(sval)
        nowtime = int(time.mktime(time.strptime( time.strftime(xlServerCopy.ISOTIMEFORMAT), xlServerCopy.ISOTIMEFORMAT)))
        for k, v in xlServerCopy.lastRTime.iteritems():
            if k not in xlServerCopy.host:
                if (nowtime - v) > 1.5*xlServerCopy.MaxInterVal:
                    xlServerCopy.host[k] = 0
                else:
                    isEnd = False

        if isEnd:
            xlServerCopy.allFinished = True
            break

#log
    dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fp = open("./logInfo/runlog.txt","w")
    fp.write("finished" +"\r"+dt+"\n")
    fp.close()
    nowtime = int(time.mktime(time.strptime(time.strftime(xlServerCopy.ISOTIMEFORMAT), xlServerCopy.ISOTIMEFORMAT)))
    Time = time.strftime('%Y-%m-%d')
    zerotime = int(time.mktime(time.strptime(Time+" 00:00:00", xlServerCopy.ISOTIMEFORMAT)))

    stime = int(86400 - (nowtime - zerotime)/2)
    time.sleep(stime)

    """重启主机"""
    xlServerCopy.host.clear()
    xlServerCopy.lastRTime.clear()
    xlServerCopy.finished = 0
    xlServerCopy.allFinished = False
    xlServerCopy.MaxInterVal = 0
    xlServerCopy.notJudgeRun = True
    xlServerCopy.runJudge = -1
