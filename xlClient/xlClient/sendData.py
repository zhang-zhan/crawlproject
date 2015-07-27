# -*- coding: utf-8 -*-
import sys
from suds.client import Client

import suicide
import datetime
__author__ = 'jiaodongdong'

#sclient=Client('http://192.168.8.3:7789/SOAP/?wsdl')

def insert_log(record):
    '''
    打印错误日志
    '''
    with open('/home/ubuntu/S_spider/logs/sendToWeb.log', 'a') as log:
        log.write('{time},{record},\r\n'.format(
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            record = record
        ))

def sendToWeb(name,at,text,sclient):
	#print 'SEND'
	sec = '【新浪微博】'
	if suicide.hasSuicidal(text) is False:
		return

	#print name, text, at, sec
	trytimes = 3
	while trytimes > 0:
	    trytimes -=1
	    try:
		sclient.service.sendData(name, text, at, sec)
		break
	    except Exception as e:
		print 'service Error:',e
		insert_log('service Error: %s' % str(e))
		if trytimes == 1:
		    print 'reconnect'
		    insert_log('reconnect webservice')
		    sclient=Client('http://192.168.8.3:7789/SOAP/?wsdl')

