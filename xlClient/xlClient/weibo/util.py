# -*- encoding=utf-8 -*-
__author__ = 'Peter'

import os,codecs,urllib2
import os.path, time, struct
from datetime import datetime

def get_user_path_list(base_dir, dir='/'):
    uids = get_lines(base_dir+'/TaskList.txt')

    updic = dict()
    for uid in uids:
        if not dir.startswith('/'):
            dir = '/' + dir
        if not dir.endswith('/'):
            dir = dir + '/'
        updic[uid] = base_dir + dir + uid
    return updic

def get_lines(path_txt):
    lines = set()
    with codecs.open(path_txt,'r',encoding='utf-8-sig') as f:
        for line in f:
            e = line.strip(' \t\r\n')
            if len(e)>0:
                lines.add(e)

    return lines

def time_format(time_str):
    """Process the datetime format in Weibo and return epoch format."""
    #dateti = time_str.replace('[+-]\w\w\w\w\s', '')
    if isinstance(time_str,unicode):
        time_str = time_str.encode()

    if isinstance(time_str,str):
        d = time_str.split(" ")
        zone = d.pop(4) #time zone
        time_str = "%s %s %s %s %s" % tuple(d)
        dtmp = datetime.strptime(time_str, "%a %b %d %X %Y")

        stamp = int(time.mktime(dtmp.timetuple()))
        if zone != "+0800":
            hour = int(zone[1: 3])
            min  = int(zone[3: 5])
            stamp += min*60 + (hour+8)*3600 if zone[0] is '-' else (hour-8)*3600
    else:
        stamp = int(time.mktime(time_str.timetuple()))

    stamp = time.strftime("%Y/%m/%d", time.localtime(stamp))
    return stamp

def time2epoch(time_str):
    """Process the datetime format in Weibo and return epoch format."""
    #dateti = time_str.replace('[+-]\w\w\w\w\s', '')
    if isinstance(time_str,unicode):
        time_str = time_str.encode()

    if isinstance(time_str,str):
        time_str = time_str.strip(' \t\r\n')
        if len(time_str)<1:
            print("Got empty time string!")
            return -1

        d = time_str.split(" ")

        zone = d.pop(4) #time zone

        time_str = "%s %s %s %s %s" % tuple(d)
        dtmp = datetime.strptime(time_str, "%a %b %d %X %Y")

        stamp = int(time.mktime(dtmp.timetuple()))
        if zone != "+0800":
            hour = int(zone[1: 3])
            min  = int(zone[3: 5])
            stamp += min*60 + (hour+8)*3600 if zone[0] is '-' else (hour-8)*3600
    else:
        stamp = int(time.mktime(time_str.timetuple()))
    return stamp

def time2str(time_str=None):
    """Process the datetime format in datetime.datetime or epoch and return Weibo format str."""
    if isinstance(time_str,str):
        #Convert from string to epoch
        dtmp = datetime.strptime(time_str, "%a %b %d %X %Y")
        time_str = int(time.mktime(dtmp.timetuple()))
    elif isinstance(time_str,datetime):
        time_str = int(time.mktime(time_str.timetuple()))
    elif time_str is None:
        time_str = int(time.mktime(time.localtime()))
    return time.strftime("%a %b %d %X +0800 %Y", time.localtime(time_str))


def get_mtime(path):
    """Return the time of last modification of path as epoch format."""
    mtime = time.ctime(os.path.getmtime(path))
    dtmp = datetime.strptime(mtime, "%a %b %d %X %Y")
    stamp = int(time.mktime(dtmp.timetuple()))
    return stamp

def now2epoch():
    now = time.mktime(time.localtime())
    return int(now)

def convert_endian(v):
    f = None
    if isinstance(v, int):
        f = '<i'
    elif isinstance(v, long):
        f = '<q'
    else:
        raise ValueError('Unsupported type to convert endian: %s' % type(v) )

    if f is not None: v = buffer(struct.pack(f, v))
    return v

def unpack_little_endian(v):
    n = len(v)/8
    f = struct.unpack_from('<' + 'q'*n, v)
    return f

def store_image(source_url,dest_fname,headers=None):
    head = {}
    if headers is not None:
        head.update(headers)

    data = 3
    while data>0:
        data -= 1
        try:
            req = urllib2.Request(source_url, None, head)
            data=urllib2.urlopen(req).read()
            break
        except Exception as e:
            print('Unable to download image [Time:%d][%s]' % (data,source_url))
            #raise RuntimeWarning('Unable to download image [%s]' % source_url)

    if isinstance(data,int):
        print('Unable to save image [%s]' % source_url)
        return False

    fout = file(dest_fname,"wb")
    fout.write(data)
    fout.close()
    return True