__author__ = 'zhangzhan'
import sys
import MySQLdb

def rtoken():
    try:
        conn = MySQLdb.connect(host = "192.168.8.1",
                               user = "psymap",
                               passwd = "wsi_208",
                               db = "psymap")
    except MySQLdb.Error,e:
        print "Error %d:%s"%(e.args[0],e.args[1])
        sys.exit(1)
    try :
        cursor = conn.cursor()
        cursor.execute("select Token from userlink where SiteType = 'SINA ' ORDER  BY Updated DESC LIMIT 0,200")
    except :
          conn.close ()

    token = []
    i = 0
    row = cursor.fetchone ()
    while i< 200:

        if row != None:
            token.append(row[0])
        else:
            cursor.execute("select Token from userlink where SiteType = 'SINA 'ORDER  BY Updated DESC LIMIT 0,200")
            row = cursor.fetchone ()
            token.append(row[0])
        row = cursor.fetchone ()
        i += 1
    return token
