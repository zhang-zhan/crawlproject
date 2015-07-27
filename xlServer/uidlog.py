import codecs
# -*- coding: utf-8 -*-

class Suid:
     def suid(self,uid,error,time,judge):
         fp = codecs.open("logInfo/uidlog.txt","a")
         fp2 = codecs.open("logInfo/userUnused.txt","a")    #存储未使用的uid
         fp.write(uid+'\t'+error+'\t'+time+"\n")
         fp2.write(uid+"\n")
         fp.close()
         fp2.close()
