__author__ = 'zhangzhan'
# -*- coding: UTF-8 -*-
import json
import codecs
from util import *
from weibo import Status
from hbase import gateway
from hbase import ttypes
import urllib2
import urllib
import time
import sys
import socket
import datetime
import date2stamp
from xlRequest import *
reload(sys)
sys.setdefaultencoding('utf8')


from sendData import sendToWeb
sendData = True

from suds.client import Client
#sclient=Client('http://192.168.8.3:7789/SOAP/?wsdl')

import suicide
suicide.initSuicidalJudge()


def error_log(record):
    '''
    打印错误日志
    '''
    with open('/home/ubuntu/xlClient/logs/error.log', 'a') as log:
        log.write('{time},{record},\r\n'.format(
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            record = record
        ))

def run_log(record):
    '''
    打印错误日志
    '''
    with open('/home/ubuntu/xlClient/logs/run.log', 'a') as log:
        log.write('{time},{record},\r\n'.format(
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            record = record
        ))

def process_item():

    hclient = gateway.HBaseClient()
    allcount = 0
    uidCount = 0
    sCount = 0
    retweetCount = 0

    socket.setdefaulttimeout(60)

    while(True):

        Request = None
        Request = urlRequest()
        Request = Request.getRequest()
        run_log("Request")
        """对获取的Request进行判断"""
        try:
            if isinstance(int(Request),int):

                time.sleep(int(Request))
                continue
        except:
            print

        if Request != None:

            uidCount += 1	#统计用户个数
            statuses = None	#
            statusCount = 0	#统计微博个数
            pageCount = 1	#设置起始页数为1
            infoDict = {}	#把一个用户的微博信息先存放在dict中，在存入数据库
            sCount = 0

            """判断在数据处理过程中是否发生错误Jd"""
            hasError = False
            limitFalse = False
            notenough = False
            isFirst = True
            lastUpdate = 0

            create_time = 0

            """用户uid，access_token,request"""
            timeUid =None
            token = None
            request = None
            timeUid = Request['uid']
            token = Request["token"]
            requestUrl = Request['url']

            """获取上次更新的时间jd"""
            nowtime = hclient.getUpdateTime('sina_user', timeUid)
            #nowtime = hclient.getUpdateTime('TimePoint', timeUid, 'f:old')

            """对一个用户进行循环下载微博数据"""

            while(True):
                request = requestUrl+str(pageCount)
                print request
                run_log("download")

                max = 5
                statuses = None

                """ 下载微博数据"""

                while(max > 0):

                    max -= 1
                    try :
                        statuses = urllib.urlopen(request).read()
                        statuses = json.loads(statuses, encoding='utf-8')
                        if pageCount < 11 and statuses.get('statuses', 1) == 1:
                            error_log("WARN:%s cannot get statuses,but maybe load finish" % timeUid)
                            time.sleep(3)
                            continue
                        break
                    except Exception as e:
                        error_log("FATAL:%s cannot get statuses" % timeUid)

                """ 微博数据不为空"""
                if statuses != None:

                    """出现错误"""
                    if "error" in statuses:   #judge error exit.

                        dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        hasError = True

                        #if statuses["error"] == "expired_token": # token is expired 权限为15天的token

                            # error_log("ERROR:expired_token")
                            # req = "http://192.168.21.162:8080/rec_uid_access"
                            # data = {}
                            # data["access_token"] = token
                            # data["uid"] = timeUid
                            # data["error"] = statuses["error"]
                            # data["time"]  = dt
                            # data = json.dumps(data,sort_keys=True)
                            #
                            # try:
                            #     req = urllib2.Request(req,data)
                            #     resp = urllib2.urlopen(req)
                            #     resp.close()
                            #     req.close()
                            #     #resp.close()
                            #     break
                            # except Exception:
                            #     error_log("FATAL:failed to send failed token % s" % timeUid)
                            #     break
                        if statuses["error"] == "User requests out of rate limit!":
                            time.sleep(180)
                            limitFalse = True


                        elif statuses["error"] == "source paramter(appkey) is missing":  #权限为一天的token过期

                            error_log("ERROR:source paramter(appkey) is missing")
                            req = "http://192.168.21.162:8080/rec_uid"
                            u_info = {}
                            #u_info["uid"] = timeUid
                            u_info["access_token"] = token
                            #u_info["error"] = statuses["error"]
                            #u_info["time"] = dt
                            u_info["errorType"] = 1
                            u_info = json.dumps(u_info,sort_keys=True)

                            try:
                                req = urllib2.Request(req,u_info)
                                resp = urllib2.urlopen(req)
                                resp.close()
                                req.close()
                                break
                            except Exception as e:
                                error_log("FATAL:Failed to handle day token %s" % timeUid)
                                break

                        # elif statuses["error"] == "User does not exists!": #用户不存在
                        #
                        #     error_log("ERROR:User does not exists! %s" % timeUid)
                        #     req = "http://192.168.21.162:8080/rec_uid_nexist"
                        #     uid_info = {}
                        #     uid_info["error"] = statuses["error"]
                        #     uid_info["uid"] = timeUid
                        #     uid_info["time"] = dt
                        #     uid_info = json.dumps(uid_info,sort_keys=True)
                        #
                        #     try:
                        #         req = urllib2.Request(req,uid_info)
                        #         resp = urllib2.urlopen(req)
                        #         resp.close()
                        #         req.close()
                        #         break
                        #     except Exception as e:
                        #         error_log("FATAL::User does not exists! %s" % timeUid)
                        #         break

                            """出现其他一些错误"""
                        # else:
                        #
                        #     error_log("ERROR:-other- %s" % statuses["error"])
                        #     req = "http://192.168.21.162:8080/rec_uid_other"
                        #     u_info = {}
                        #     u_info["uid"] = timeUid
                        #     u_info["error"] = statuses["error"]
                        #     u_info["time"] = dt
                        #     u_info = json.dumps(u_info,sort_keys=True)
                        #
                        #     try:
                        #         req = urllib2.Request(req,u_info)
                        #         resp = urllib2.urlopen(req)
                        #         resp.close()
                        #         req.close()
                        #         break
                        #     except Exception as e:
                        #         error_log("FATAL: handle other")
                        #         break


                    else:       #微博未出现错误

                        statuses = statuses.get('statuses', [])
                        judgement = False

                        if statuses == []:
                            error_log("WARN:statuses is []")
                            notenough = True
                            break

                        else:  #解析微博数据，并将它存入数据库

                            for s in statuses:   #获取每条微博
                                uid = s['user']['id']
                                u_name = s['user']['name']
                                create_time = s['created_at']  #

                                create_time = date2stamp.date2unix(create_time)

                                """对微博时间与以下载时间进行比较"""
                                if create_time > nowtime:
                                    sCount += 1
                                    statusCount += 1
                                    judgement = True

                                    if isFirst:
                                        lastUpdate = create_time
                                        isFirst = False

                                    """微博中有转发"""
                                    if 'retweeted_status' in s:
                                        retweetCount += 1

                                    """删除微博中的重复数据,只保留用户uid"""
                                    if statusCount > 1:
                                        del s['user']
                                        s['uid'] = long(uid)

                                        if 'retweeted_status' in s:

                                            if 'user' in s['retweeted_status']:
                                                ruid = s['retweeted_status']['user']['id']
                                                del s['retweeted_status']['user']
                                                s['retweeted_status']['uid'] = long(ruid)

                                    """ 连接数据库"""
                                    try:
                                         r_status = Status()
                                         r_status.load(s)

                                         batches = r_status.get_batches()

                                         for batch in batches:
                                             tableName = batch['tableName']
                                             rowBatches = batch['rowBatches']

                                             if infoDict.has_key(tableName):
                                                 infoDict[tableName].append(rowBatches)
                                             else:
                                                 infoDict[tableName] = [rowBatches]
                                    except Exception as e:
                                         error_log("ERROR:-analyze- %s" % e.message)
                                         continue
                                    """发送数据到suidice"""
                                    #print "SENDDATA"
                                    #if sendData is True:
                                        #try:
                                            #print "ss"
                                            #sendToWeb(u_name,s['created_at'],s['text'],sclient)
                                            #print "ss2"
                                        #except Exception as e:
                                            #error_log("ERROR:-suicide-- %s" % e.message)
                                            #continue
                                    """若时间小于已下载微博的时间，就下载另一个用户微博"""
                                else:
                                    judgement = False
                                    break

                            """判断是否出错，没有就页数加1，下载另一页"""
                            if judgement == False:
                                break
                            else:
                                if limitFalse is False:
                                    pageCount += 1

                else:
                    #微博数据为空就把用户uid返回给服务器进行重新下载

                    break
                    # dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # hasError = True
                    # req = "http://192.168.21.162:8080/rec_uid_other"
                    # u_info = {}
                    # u_info["uid"] = timeUid
                    # u_info["error"] = "statuses is None"
                    # u_info["time"] = dt
                    # u_info = json.dumps(u_info,sort_keys=True)
                    #
                    # try:
                    #     req = urllib2.Request(req,u_info)
                    #     resp = urllib2.urlopen(req)
                    #     resp.close()
                    #     req.close()
                    #     break
                    # except Exception as e:
                    #     error_log("FATAL:failed reload UID %s" % timeUid)
                    #     break

            """如果没有发生错误，则更新数据库"""
            if hasError is False:
                hclient.applyBatch(infoDict)
                if lastUpdate > nowtime:
                    hclient.setUpdateTime('sina_user',timeUid,lastUpdate)
                else:
                    error_log("FATAL:FAILED UPDATE UPDATETIME %s" % timeUid)
                #hclient.setTimePoint('TimePoint', timeUid, lastUpdate, 'f:end')

                #run_log("insertHbase")

                #"""这部分在第一下载是有用，以后更新下载没用"""
                #"""
                #if notenough:
                    #oldTime = create_time
                    #print 'oldTime',oldTime
                    ##测试阶段不更新
                    #run_log("insertTimePoint")
                    #hclient.setTimePoint('TimePoint', timeUid, oldTime, 'f:beg')
                #"""
            allcount += sCount

        else:
            time.sleep(30)

        print "[Number of uid]::%s"%uidCount
        #print uidCount
        print "[Number of status]::%s"%sCount
        #print sCount
        print "[Number of retweeted_status]::%s"%retweetCount
        #print retweetCount

    hclient.clientClose()

if __name__ == "__main__":
    process_item()
