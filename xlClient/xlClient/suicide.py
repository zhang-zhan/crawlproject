keywords = []

def initSuicidalJudge():
    global keywords
    keywordstmp = open("./dic/dic1.txt").readlines()
    for w in keywordstmp:
        keywords.append(w.decode('GBK').encode('UTF-8').strip())

def hasSuicidal(text):
    global keywords
    for w in keywords:
        if text.find(w) >= 0:
            return True
    return False
