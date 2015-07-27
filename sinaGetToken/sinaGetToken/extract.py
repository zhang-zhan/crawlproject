__author__ = 'zhangzhan'

# fr = open("./userpwd/8.txt","r")
# fR = open("./newFile/8.txt","r")
# fw = open("./newFile/all.txt","a")
# orText = fr.readlines()
# newText = fR.readlines()
# print len(newText),len(orText)
# i = 0
# j = 0
# while True:
#     if i == len(newText):
#         break
#
#     user1,pwd1 = newText[i].strip().split("\t")
#     user2,pwd = orText[j].strip().split("\t")
#     print i,j,user1,user2
#     if user1 == user2:
#         j += 1
#         i += 1
#         fw.write(user1+"\t"+pwd+"\n")
#     else:
#         j += 1

# fr  = open("./newFile/all.txt","r")
# lines = fr.readlines()
# l = len(lines)+1
#
# for i in range(1,l):
#     fw = open("./userinfo/%s.txt"%(i%46),"a")
#     user,pwd = lines[i-1].strip().split("\t")
#     fw.write(user+"\t"+pwd+"\n")
#     fw.close()

fr = open("test.txt","w")
fr.truncate()
fr.close()

fr = open("test.txt","a")
fr.write("OOOOOOOOOOOOOOOO")