# -*- coding: utf-8 -*-
from misc import alphabet,finder

class Options(list):
   #Creates and manages an option list
    def __init__(self,lang="english",heading="",footing=""):
        self.lang = lang
        self.position = 0
        self.heading = heading
        self.footing = footing

    def add_Option(self,content):
        ab = alphabet(self.lang)
        alpha= ab.retstr()
        letter = alpha[len(self)]
        line = [letter,content.decode('utf-8')]
        self.position+=1
        self.append(line)
        
    def print_Options(self):
        strn=""
        for i in self:
            strn+=i[0]+") " +i[1] + "\n"
        return strn

    def select_Option(self,opts):
        disp = Chunks(opts);disp.create_Chunks(footing=self.footing,heading="");i=0
        print self.heading
        while i < len(disp.chunk_list):
            print disp
            nekst = raw_input("SMS in: ")
            bacfin = finder(r'back',nekst)
            if bacfin.found():
                if disp.position == 0:
                    continue
                else:
                    i-=1; disp.position-=1;continue
            finfin = finder(r'^find',nekst.lower())
            if finfin.found():
                print "found on these pages:"
                print ", ".join([i for i in disp.find_Chunks(nekst[finfin.endpos()+1:])])
                continue
            exifin = finder(r'exit',nekst.lower())
            if exifin.found():
                return 'exit'
            disp.position+=1;i+=1
            
            for j in range(len(self)):
                if nekst.lower() == self[j][0]:
                    return j
        return None
        
    def __list__(self):
        return self
        
#test = Options()
#test.add_Option("0 - Ratings : 1")
#print test
#for j in [1,2,3,4]:
#    if opts == None:
#        opts = Options(heading="By ({0}) Did you mean: ".format('test'),
#                           footing="Please choose.")
#    opts.add_Option(content="{0}".format(j))
#    
#    if opts:
#                ch = opts.select_Option(opts.print_Options())
#                corr.append([i,str(opts[ch][1])])
#            opts = None
#        print corr
#        for k in corr:
#            if str(k[1]) in self.corrected:
#                self.corrected[str(k[1])]= [k[0]]
#            else:
#                self.corrected[str(k[1])].append(k[0])
#        return com.disting(command)['words']           


class Chunks(str):
    def __init__(self,text):
        self.size = 140
        self.text = text
        self.chunk_list=[]
        self.position=0
    
    def __str__(self):
        if len(self.chunk_list)==0:
            return ""
        else:
            return self.chunk_list[self.position%len(self.chunk_list)]
        
    def create_Chunks(self,footing="",heading=""):
        if len(heading)>0:
            heading = heading+"\n"
        if len(footing)>0:
            footing = "\n"+footing
            
        chunks = []
        chunksize = self.size - (len(heading)+len(footing))
        maxpos = len(self.text)/chunksize
        lastsize = len(self.text)%chunksize
        temp = ""
        for i in range(maxpos+1):
            if i == maxpos:
                temp = heading + self.text[(i*chunksize):((i*chunksize)+lastsize)] + footing
                if len(temp)>0:
                    chunks.append(temp)
                break
            temp = heading + self.text[(i*chunksize):((i+1)*chunksize)] + footing
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
    
    def display_Chunks(self):
        i=0
        while i < len(self.chunk_list)-1:
            print self
            nekst = raw_input("SMS in: ")
            bacfin = finder(r'back',nekst)
            if bacfin.found():
                if self.position == 0:
                    continue
                else:
                    i-=1; self.position-=1
            finfin = finder(r'find',nekst)
            if finfin.found():
                print "found on these pages:"
                print ", ".join([i for i in self.find_Chunks(nekst[finfin.endpos():])])
                continue
            exifin = finder(r'exit',nekst)
            if exifin.found():
                return None
            self.position+=1;i+=1    
        return None
        
    

#testtext="""athethaethaeathethaethaeathethaethaeathethaethaeathethaetha
#eathethaethaeathethaethaeathethaethaeathethaethaeathethaethaeathethaethae
#athethaethaeathethaethaeathethaethaeathethaethaeathethaethaeathethaethaeath
#athethaethaeathethaethaeathethaethaeathethaethaeathethaethaeathethaethaea
#athethaethaeathethaethaeathethaethaeathethaethaeathethaethaeathethaethae
#\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"""
#
#test = Chunks(testtext)
#test.create_Chunks(footing="test text:")
#
#test.display_Chunks()
#
#
#print map(lambda x:len(x),test.chunk_list)
#print test.find_Chunks('athe')
