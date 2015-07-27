__author__ = 'jiaodongdong'
#encoding=utf-8
from datetime import datetime
import time
def date2unix(attr):
    dalist = attr.split()
    
    zone = dalist[4]
    datef = dalist[0]+" "+dalist[1]+" "+dalist[2]+" "+dalist[3]+" "+dalist[5]

    dtmp = datetime.strptime(datef, "%a %b %d %X %Y")
    stampt = int(time.mktime(dtmp.timetuple()))
    if zone is "+0800":
        return stampt
    else:
        hou = int(zone[1: 3])
        mint = int(zone[3: 5])
        if zone[0] is '-':
            return (hou+8)*3600+mint*60+stampt
        else:
            return stampt - ((hou-8)*3600+mint*60)

