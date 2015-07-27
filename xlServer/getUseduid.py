
import codecs


def openfile():
    fp = codecs.open("logInfo/UidUsedlog.txt","r")
    number = 0
    for line in fp:
        line = line.strip("\t\r\n")
        if line != "":
            number += 1
        else:
            break
    
    fp.close()
    num = openuid()
    if number == num:
        fp = codecs.open("logInfo/UidUsedlog.txt","r+")
        fp.truncate()
        fp.close()
        return "no"
    else:
        return number

def openuid():
    fp = codecs.open("uid/undownload.txt","r")
    count = 0
    for line in fp:
        line = line.strip("\t\r\n")
        if line != "":
            count += 1
        else:
            break

    fp.close()
    return count
