__author__ = 'zhangzhan1'
# -*- coding: utf-8 -*-

from xlDownload import *
from SocketServer import ThreadingMixIn
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from SocketServer import TCPServer
import SimpleXMLRPCServer
import os
import socket
import fcntl
import struct
import urllib2
import threading
import urllib2
import urllib
import socket
import logging
import gzip
import uuid
import re
import time
import json

ISOTIMEFORMAT = '%Y-%m-%d %X'
TCPServer.request_queue_size = 10000
state = 'True'

def runspider():
   try:
    os.system('python xlDownload.py')
   except  AttributeError: 
    print " I got mistake"

def stopspider():
    lines = os.popen('ps -ef|grep c_download')
    for line in lines:
       if line.find('grep c_download')!=-1: continue
       vars = line.split()
       pid = vars[1] #get pid
       proc = ''.join(vars[7:]) #get proc description

       out = os.system('kill -9 '+pid)
       if out==0:
          print('success! kill '+pid+' '+proc)
       else:
          print('failed! kill '+pid+' '+proc)

class MyObject:
    def run(self):
        global state
        if state == 'True':
           state = 'False'
           tr = threading.Thread(target=runspider)
           tr.start()
	return 'ok'

    def stop(self):
        global state
        if state == 'False':
           state = 'True'
           ts = threading.Thread(target=stopspider)
           ts.start()
        return 'ok'

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

class Util(threading.Thread):

    getIpAddr = 'http://www.ip.cn/'

    def readHTTPBody(self,obj, decodeType=None):
        using_gzip = obj.headers.get('Content-Encoding', '') == 'gzip'
        body = obj.read()
        if using_gzip:
           logging.info('gzip content received.')
           gzipper = gzip.GzipFile(fileobj=io.BytesIO(body))
           fcontent = gzipper.read()
           fcontent = fcontent.decode(decodeType)
           gzipper.close()
           return fcontent
        return body.decode(decodeType)

    '''def getSelfRemoteIP(self):
        req = urllib2.Request(self.getIpAddr)
        resp = urllib2.urlopen(req,timeout=5)
        body = self.readHTTPBody(resp,'utf-8')

        ipPattern='(([0-9]{1,3}.){3}[0-9]{1,3})'
        m = re.search(ipPattern, body)
        if m is not None:
            return m.group()
        else:
            return None'''

    def get_ip_address(self,ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


    def getSelfMAC(self):
        node = uuid.getnode()
        mac = uuid.UUID(int = node).hex[-12:]
        return mac

    def getHostName(self):
        hostname = socket.gethostname()
        return hostname
    def getStateCrawler(self):
        global state
        t = return_state()
        return t

    def getSelfInfo(self):
        global state
        i = {}
        i['HostName']  = self.getHostName()
        i['MAC']       = self.getSelfMAC()
        i['IPLocal']   = self.get_ip_address('eth0')
        i['IPRemote']  = "no" #self.getSelfRemoteIP()
        i['Port']      = self.getStateCrawler()
        i['sendtime']  = time.mktime(time.strptime( time.strftime(ISOTIMEFORMAT), ISOTIMEFORMAT ) )
        i['state']     = state
        return i

    def run(self):
        while True:
          req = "http://192.168.8.100:8080/request"
          u = Util()
          info = u.getSelfInfo()
          data = json.dumps(info,sort_keys=True)
          try:
             req = urllib2.Request(req,data)
             resp = urllib2.urlopen(req)
             print ' I am working'
          except Exception:
             print ' the server is offline'

          import time
          time.sleep(15)


def start():
    obj = MyObject()
    port = 10090
    local_ip = get_ip_address('eth0')
    print local_ip

    server = SimpleXMLRPCServer.SimpleXMLRPCServer((local_ip, port),SimpleXMLRPCRequestHandler,False)
    server.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.register_instance(obj)
    print "Listening on port 10090"
    server.serve_forever()



t1 = Util()
t1.start()
t2 = threading.Thread(target=start)
t2.start()

