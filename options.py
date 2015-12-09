# -*- coding: utf-8 -*-
from misc import alphabet,finder

class Options(list):
   #Creates and manages an option list
    def __init__(self,lang="english",heading="",footing=""):
        self.lang = lang
        self.position = 0
        self.heading = heading
        self.footing = footing

    def add_Option(self,content,title=""):
        ab = alphabet(self.lang)
        alpha= ab.retstr()
        letter = alpha[len(self)]
        line = [letter,title.decode('utf-8'),content.decode('utf-8')]
        self.position+=1
        self.append(line)
        
    def print_Options(self):
        strn=self.heading+"\n"
        for i in self:
            strn+=i[0]+") " +i[1]+" - "+i[2]+"\n"
        strn+=self.footing
        return strn

    def select_Option(self,opts):
        disp = Chunks(opts.print_Options);disp.create_Chunks()
        while i < len(disp.chunk_list):
            print disp
            nekst = raw_input("SMS in: ")
            bacfin = finder(r'back',nekst)
            if backfin.found():
                if disp.position == 0:
                    continue
                else:
                    i-=1; disp.position-=1
            finfin = finder(r'find',nekst)
            if finfin.found():
                print "found on these pages:"
                print ", ".join([i for i in disp.find_Chunks(nekst[finfin.endpos():])])
            exifin = finder(r'exit',nekst)
            if exifin.found():
                break
            disp.position+=1;i+=1
        
        choice = raw_input("SMS in: ")
        for i in range(len(self)):
            if choice.lower() == self[i][0]:
                return i
            
    def __list__(self):
        return self
        
#test = Options()
#test.add_Option("0 - Ratings : 1")
#print test
           


class Chunks(str):
    def __init__(self,text,footing="",heading=""):
        self.heading = heading
        self.footing = footing
        self.size = 140
        self.text = text
        self.chunk_list=[]
        self.position = 0
    
    def __str__(self):
        if len(self.chunk_list)==0:
            return ""
        else:
            return self.chunk_list[self.position%len(self.chunk_list)]
        
    def create_Chunks(self):
        if len(self.heading)>0:
            self.heading = self.heading+"\n"
        if len(self.footing)>0:
            self.footing = "\n"+self.footing
            
        chunks = []
        chunksize = self.size - (len(self.heading)+len(self.footing))
        maxpos = len(self.text)/chunksize
        lastsize = len(self.text)%chunksize
        temp = ""
        for i in range(maxpos+1):
            if i == maxpos:
                temp = self.heading + self.text[(i*chunksize):((i*chunksize)+lastsize)] + self.footing
                if len(temp)>0:
                    chunks.append(temp)
                break
            temp = self.heading + self.text[(i*chunksize):((i+1)*chunksize)] + self.footing
            chunks.append(temp)

        for i in range(len(chunks)):

            if chunks[i][-1] == "\\" and chunks[i+1][0] == "n":
                if (lastsize+1)>chunksize:
                    chunks.append("")
                j=len(chunks)-1
                while i<j<len(chunks):
                    chunks[j]=chunks[j-1][-1]+chunks[j][1:];j-=1

        self.chunk_list = chunks
        
    def find_Chunks(self,word):
        res=[]
        for i in range(len(self.chunk_list)):
            findword = finder(r'{0}'.format(word.lower().decode('utf-8')),self.chunk_list[i])
            if findword.found():
                res.append([len(findword.findall()),i])
        return res
        
    
    

#test = Chunks("""athethaethaeathethaethaeathethaethaeathethaethaeathethaetha
#eathethaethaeathethaethaeathethaethaeathethaethaeathethaethaeathethaethae
#athethaethaeathethaethaeathethaethaeathethaethaeathethaethaeathethaethaeath
#athethaethaeathethaethaeathethaethaeathethaethaeathethaethaeathethaethaea
#athethaethaeathethaethaeathethaethaeathethaethaeathethaethaeathethaethae
#\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n""")
#test.create_Chunks()
#
#print test,test.position
#test.position+=1
#print test,test.position
#test.position+=1
#print test,test.position
#test.position+=1
#
#
#print map(lambda x:len(x),test.chunk_list)
#print test.find_Chunks('athe')
