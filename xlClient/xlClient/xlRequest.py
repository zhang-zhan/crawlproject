__author__ = 'zhangzhan1'
# -*- coding: utf-8 -*-
#from scrapy.http.request import *
import urllib2
import json
import Queue
import string
import codecs
import socket
urlqueue = Queue.Queue(maxsize = 1000)

def getHostName():
	hostname = socket.gethostname()
	index = len(hostname)
	return str(hostname[11:index])

url = 'http://192.168.21.162:8080/hostname='+getHostName()

class urlRequest:

    def getRequest(self):
        global urlqueue
        if urlqueue.empty():
            data = None
            max_try = 3
            while max_try > 0:
                max_try -= 1
                try:
                    st = urllib2.urlopen(url)
                    data = st.read()
                    st.close()
                    break

                except Exception as e:
                    print 'get_request ERROR'
            if data is None:
                return None
            #print type(data)
            if data == 'None':
                return None
            try:
                if isinstance(int(data),int):
                    return int(data)
            except:
                print "it is not int"

            try:
                datas = json.loads(data.replace("\'", '"'),encoding='utf-8')
                value = datas['values']
                token = []
                token = datas['token']
                tlength = len(token)
                length = len(value)
                handler = datas['handler']
                if handler == 'statuses':
                    for i in range(0,length):
                        data = dict()
                        v =(str(value[i][0]),str(token[i%tlength]))
                        url_template = str(datas['url_template'])

                        url_template = url_template.format(*v)
                        #print url_template
                        data['url'] = url_template
                        data['token']   = token[i%tlength]
                        data['uid'] = str(value[i][0])
                        urlqueue.put(data)
                    #print data
                    data = urlqueue.get()
                    return data

                elif handler == 'profile':
                    for i in range(0,length):
                        data = dict()
                        v =(value[i],datas['token'])
                        url_template = datas['url_template']
                        url_template = url_template.format(*v)
                        data['url'] = url_template
                        data['wait']   = datas['wait']
                        #data['method'] = method
                        urlqueue.put(data)

                    data = urlqueue.get()
                #return Request(url=data['url'],method=data['method'])
                elif handler == 'tags':
                    for i in range(0,length):
                        data = dict()
                        v =(str(value[i]),str(datas['token']))
                        url_template = datas['url_template']
                        url_template = url_template.format(*v)
                        data['url'] = url_template
                        data['wait']   = datas['wait']

                        #data['method'] = method
                        urlqueue.put(data)

                    data = urlqueue.get()
                    #return Request(url=data['url'],method=data['method'])

            except ValueError:
                 return None

        else:
            data = urlqueue.get()
            return data


