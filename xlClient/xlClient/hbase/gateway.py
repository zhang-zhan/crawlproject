# -*- coding: UTF-8 -*-
__author__ = 'jiaodongdong'

import Hbase
from ttypes import *
from thrift.transport import *
import struct
import datetime
import random

port = 9090
hosts = ['192.168.9.%d' % i for i in range(1,45)]

def error_log(record):
    '''
    打印错误日志
    '''
    with open('/home/ubuntu/S_spider/logs/Hbaserror.log', 'a') as log:
        log.write('{time},{record},\r\n'.format(
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            record = record
        ))

class HBaseClient:
    def __init__(self, index=0):
	if index==0:
		index = random.randint(0,120) % 44

        address = HBaseClient.cfg[index]['host']
        port = HBaseClient.cfg[index]['port']
        self.index = index
        self.transport = TTransport.TBufferedTransport(TSocket.TSocket(address, port))
        self.protocol = TBinaryProtocol.TBinaryProtocolAccelerated(self.transport)

        self.client = Hbase.Client(self.protocol)
        self.transport.open()

    def reconnect(self):
        try:
            self.transport.close()
        except Exception as e:
            print e
	    error_log("ERROR:%s" % e.message)

        maxTry = 100
        while True:
            maxTry -= 1
            if maxTry < 0:
                exit(1)
            try:
                self.index = (self.index+1)% len( HBaseClient.cfg )
                address = HBaseClient.cfg[self.index]['host']
                port = HBaseClient.cfg[self.index]['port']

                self.transport = TTransport.TBufferedTransport(TSocket.TSocket(address, port))
                self.protocol = TBinaryProtocol.TBinaryProtocolAccelerated(self.transport)

                self.client = Hbase.Client(self.protocol)
                self.transport.open()
                break
            except Exception as e:
                print 'reconnect error:', e.message
		error_log("ERROR: -reconnect- %s" % e.message)

    def clientClose(self):
        self.transport.close()

    def getUpdateTime(self,tablename, uid, mycolumns='profile:update'):
        key = struct.pack('<q', long(uid))
        row = buffer(key)

        lastTime = 0

        trytime = 3
        while trytime > 0:
            try:
                trytime -= 1
                result = self.client.getRowWithColumns(tablename, row, [mycolumns], None)
                break
            except Exception as e:
                print 'self.client.getRow error'
		error_log("ERROR:getRowWithUpdateInfo")
                if trytime == 0:
                    self.reconnect()
                    trytime = 3

        for r in result:
            try:
                lastTime, = struct.unpack('>i', r.columns.get(mycolumns).value)
            except Exception as e:
                print 'getUpdateInfo error',e
		error_log("ERROR:getUpdateInfo")

        return lastTime

    def setUpdateTime(self,tablename, uid, oldtime, mycolumns='profile:update'):
        try:
            key = struct.pack('<q', long(uid))
            row = buffer(key)

            mutations = []

            pgb = struct.pack('>i', int(oldtime))
            pgby = buffer(pgb)
            m = Mutation(column=mycolumns, value=pgby)
            mutations.append(m)

            trytime = 3
            while trytime > 0:
                try:
                    trytime -= 1
                    self.client.mutateRow(tablename, row, mutations, None)
                    break
                except Exception as e:
                    print 'setUpdateTime self.client.mutateRow'
		    error_log("ERROR:setUpdateTime")
                    if trytime == 0:
                        self.reconnect()
                        trytime = 3
            #self.client.mutateRow(self.tableName, row, mutations, None)
        except Exception as e:
            print e
            print 'Update Info ERROR!!'
	    error_log("ERROR:Update Info ERROR!!")

    def setTimePoint(self,tablename, uid, oldtime, columnf = 'f:new'):
        try:
            key = struct.pack('<q', long(uid))
            row = buffer(key)

            mutations = []

            pgb = struct.pack('>i', int(oldtime))
            pgby = buffer(pgb)
            m = Mutation(column= columnf , value=pgby)
            mutations.append(m)

            trytime = 3
            while trytime > 0:
                try:
                    trytime -= 1
                    self.client.mutateRow(tablename, row, mutations, None)
                    break
                except Exception as e:
                    print 'self.client.mutateRow'
		    error_log("ERROR:setTimePoint mutateRow")
                    if trytime == 0:
                        self.reconnect()
                        trytime = 3
            #self.client.mutateRow(self.tableName, row, mutations, None)
        except Exception as e:
            print e
            print 'Update Info ERROR!!'
	    error_log("ERROR:Update Info ERROR!!")

    def applyBatch(self, batches):
        #print 'applyBatch'
        for tablename,rowBatches in batches.iteritems():
            print tablename, len(rowBatches)
            retryTime = 3
            while retryTime>0:
                retryTime -= 1
                try:
		    print "i am connecting"
                    self.client.mutateRows(str(tablename),rowBatches,None)
		    print "connected"
                    break
                except Exception as e:
                    print 'MutateRows Error', e
		    error_log("ERROR:MutateRows Error %s" % e.message)
                    if retryTime == 0:
                        self.reconnect()
                        retryTime = 3

HBaseClient.cfg = [{'host':host, 'port':port} for host in hosts]

