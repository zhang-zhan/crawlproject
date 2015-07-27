__author__ = 'zhangzhan1'

import codecs
import json


class baseclass:
   def __init__(self,filename):
       self.filename = filename
       self.fp = codecs.open(self.filename,'r')
       self.fr = self.fp.read()
       self.data = json.loads(self.fr.replace("\'", '"'),encoding='utf-8')
       self.fp.close()

   def get_link(self,uids,token,number):

       data = dict()
       value = list()
       data['wait']         = self.data['wait']
       data['method']       = self.data['method']
       if number == 0:
           for i in range(0,len(uids)):

                  t = [ uids[i]]
                  value.append(t)

           data['url_template'] = self.data['url_template']['statuses']
           data['token']        = token
           data['values']       = value
           data['handler']      = 'statuses'

           return json.dumps(data)
       elif number == 1:

           data['url_template'] = self.data['url_template']['profile']
           data['token']        = token
           data['values']       = uids
           data['handler']      = 'profile'

           return json.dumps(data)
       elif number == 2:

           data['url_template'] = self.data['url_template']['tags']
           data['token']        = token
           data['values']       = uids
           data['handler']      = 'tags'

           return json.dumps(data)



