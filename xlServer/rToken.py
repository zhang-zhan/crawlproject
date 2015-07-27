__author__ = 'zhangzhan1'

import codecs
from sql import *
from threading import Lock

mutex = Lock()
#tokens = []

'''with codecs.open('./conInfo/accesstoken.txt',encoding='utf-8') as f:
     for access in f:
         access_token = access.strip('\t\r\n')
         tokens.append(access_token)

def rtoken(count):
  global tokens
  with mutex:
    tList = []
    startnum = count*10
    endnum   = startnum +10
    for i in range(startnum,endnum):
	tList.append(tokens[i])
	
    return tList'''

def retToken(index):
	token = []
	with mutex:
		fr = open("./conInfo/accesstoken.txt","r")
		data = list(fr.readlines())
		fr.close()
		
		token.append(data[index].strip().split("\t")[0])
		return token
		
   

