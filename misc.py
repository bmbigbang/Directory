import re
class finder(object):
    """finder class to find text/date/time"""
    def __init__(self,r,text):
        self.r = r
        self.text=text
        self.search = re.search(self.r,self.text)
                
    def result(self):
        return self.search.string[self.search.start():self.search.end()]
    
    def remainder(self):
        if self.found():
            return self.search.string[self.search.end:]

    def findall(self):
        return re.findall(self.r,self.text)
        
    def found(self):
        if self.search:
            return True
        else:
            return False
    def endpos(self):
        if self.found():
            return self.search.end()
    def startpos(self):
        if self.found():
            return self.search.start()
    def replace(self,text):
        if self.found():
            return re.sub(r,text)

class alphabet(object):
    def __init__(self,lang):
        self.lang=lang
        self.langs = {'english':'a'}

    def retstr(self):    
        if self.lang in self.langs:
            alpha = self.langs[self.lang];finals ="";temp = int(hex(ord(alpha)),base=16)
            for i in range(26):
                finals+=unichr(temp)
                temp+= 1
            return finals
        else:
            print "language not supported"
            return None

    def choices(self,num):
        if self.lang in self.langs:
            alpha = self.langs[self.lang];finals =[];temp = int(hex(ord(alpha)),base=16)
            for i in range(num):
                finals.append(unichr(temp))
                temp+= 1
            return finals
        else:
            print "language not supported"
            return None

## test = alphabet('english')
## print test.retstr()
##test = alphabet('english')
##print test.choices(4)

