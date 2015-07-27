import codecs
# -*- coding: utf-8 -*-
#存储已返回给客户端的uid

def sUid(self,uid):
 fp = codecs.open("logInfo/UidUsedlog.txt","a")
 fp.write(uid+"\n")
 fp.close()

