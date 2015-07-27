# -*- coding: UTF-8 -*-
__author__ = 'Peter_Howe<haobibo@gmail.com>'

import sqlite3,time
from sina import APIClient

access_token = '2.002gIulCfj3PXCfbb83699c1_vP75B'

APP_KEY = 'APP_KEY'            # app key
APP_SECRET = 'YOUR_APP_SECRET'      # app secret
CALLBACK_URL = 'YOUR_CALLBACK_URL'  # callback url

mid = 3722105159602348L
ad_text = u'[%s]中科院心理所诚邀您参与心理调查～%s您只需到http://t.cn/RvKM9Tp按要求认真填写问卷(半小时内可完成),即可获赠30元话费;如有问题,请@心理地图PsyMap 。本微博转发有效,欢迎参与!如有打扰，敬请谅解。'
exps = [u'加油啊', u'太开心', u'爱你', u'鼓掌', u'来', u'呵呵', u'din分身1', u'得意地笑', u'赞啊', u'推荐', u'最右', u'羞嗒嗒', u'挤眼']

db_path = './InviteDB.db'

client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
client.access_token = access_token

def get_status_count(uid,page=5):
    result = []
    s = client.statuses.user_timeline.get(uids=uid,trim_user=1,count=200,page=page)
    print s
    ss = s['statuses']
    for s in ss:
        a = (s['id'],s['reposts_count'],s['comments_count'],s['attitudes_count'],)
        result.append(a)
    return result

def delete_empty_status():
    default_uid =  client.account.get_uid.get()

    for i in range(1,50):
        counts = get_status_count(default_uid,page=i)
        for c in counts:
            mid = c[0]
            reposts = c[1]
            comments = c[2]
            attitudes = c[3]
            reply = reposts + comments + attitudes
            print mid, reply
            if reply == 0 :
                client.statuses.destroy.post(id=mid)


def get_uids(number = 5):
    uids = []
    with sqlite3.connect(db_path) as cx:
        cur = cx.execute('SELECT Uid FROM Users WHERE NickName IS NULL ORDER BY random() LIMIT %d' % number)
        for line in cur:
            uids.append(line[0])
    return uids

def mark_uids(uid_names):
    with sqlite3.connect(db_path) as cx:
        for uid,name in uid_names.iteritems():
            cx.execute("UPDATE Users SET Invited=CURRENT_TIMESTAMP, NickName='%s' WHERE Uid='%s'" % (name,uid))

def get_screen_names(uids):
    uid_names = dict()
    for uid in uids:
        try:
            profile = client.users.show.get(uid=uid)
            screen_name = profile['screen_name']
            uid_names[uid] = screen_name
        except Exception as e:
            pass
    return uid_names

def get_mentions(uid_names):
    screen_names= ""
    for uid,name in uid_names.iteritems():
        screen_names += '@%s ' % name
    return screen_names

if __name__ == '__main__':
    import random
    i = int( random.random() )
    while True:
        uids = get_uids()
        if len(uids)==0:
            break

        uid_names = get_screen_names(uids)
        mention = get_mentions(uid_names)
        print mention

        exp =exps[i%len(exps)]
        i += 1
        txt = ad_text % (exp, mention)

        try:
            client.statuses.repost.post(id=mid, status=txt)
            mark_uids(uid_names)
            time.sleep(40)
        except Exception as e:
            e = str(e)
            print e
            if 'Text too long' in e:
                continue
            elif 'update weibo too fast' in e:
                time.sleep(120)
            else:
                break

