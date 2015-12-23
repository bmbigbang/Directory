# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 11:30:39 2015

@author: ardavan
"""
from misc import alphabet,finder

class Options(list):
   #Creates and manages an option list
    def __init__(self,lang="english",heading="",footing=""):
        self.lang = lang
        self.heading = heading
        self.footing = footing

    def add_Option(self,content,title=""):
        ab = alphabet(self.lang);alpha= ab.retstr()
        letter = alpha[len(self)]
        line = [letter,title,content.decode('utf-8')]
        self.append(line)
        
    def print_Options(self):
        strn=""; 
        for i in self:
            if i[1]:
                strn+=i[0] + ") " + i[1] + " " + i[2] + "\n"
            else:
                strn+=i[0] + ") " + i[2]+ "\n"
        return strn

    def select_Option(self,option):
        for j in range(len(self)):
            if unicode(option.lower()) == self[j][0]:
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
        content=self.text; chunks = [];added = 0;i=0
        if (len(self.text)+len(heading)+len(footing)) <= self.size:            
            self.chunk_list = [heading+content+footing]
            return None
        else:
            chunksize = self.size - (len(footing)+9)
        maxpos = (len(self.text)+len(heading))/chunksize
        lastsize = (len(self.text)+len(heading))%chunksize
        temp = heading + content[:(chunksize-len(heading))]
        if len(temp)>(chunksize-len(heading)-20):
            k = temp.find("\n",-14);finspa = len(temp.split()[-1])+1
            if k > 0:
                added +=(chunksize-k)
                temp = temp[:k]
                if len(temp) + 3 + len(footing)<=self.size:
                    chunks.append(temp+"..."+footing)
                else:
                    chunks.append(temp+footing)
                content = content[(k-len(heading)):]
            elif temp.find(" ",-10) != -1:
                added += (finspa)
                temp = temp[:-(finspa)]
                chunks.append(temp+footing)
                content = content[(chunksize-finspa):]
            elif len(temp)!=0:
                chunks.append(temp+footing);content = content[chunksize:]
        else:
            chunks.append(temp+footing);content = content[(chunksize-len(heading)):]
        if lastsize+added>chunksize:
            maxpos = (len(self.text)+len(heading)+added)/chunksize
            lastsize = (len(self.text)+len(heading)+added)%chunksize
            added = 0
        while i < maxpos+1:
            temp = content[:chunksize]
            if len(temp)>(chunksize-20):
                k = temp.find("\n",-14);finspa = len(temp.split()[-1])+1
                if k > 0:
                    added +=(chunksize-k)
                    temp = temp[:k]
                    if len(temp) + 3 + len(footing)<=self.size:
                        chunks.append(temp+"..."+footing)
                    else:
                        chunks.append(temp+footing)
                    content = content[k:]
                elif temp.find(" ",-10) != -1:
                    added += (finspa)
                    temp = temp[:-(finspa)]
                    chunks.append(temp+footing)
                    content = content[(chunksize-finspa):]
                elif len(temp)!=0:
                    chunks.append(temp+footing);content = content[chunksize:]
            elif len(temp)!=0:
                chunks.append(temp+footing);content = content[chunksize:]
            if lastsize+added>chunksize:
                maxpos = (len(self.text)+len(heading)+added)/chunksize
                lastsize = (len(self.text)+len(heading)+added)%chunksize
                added = 0
            i+=1
        counter=1;count = len(chunks)
        for i, chunk in enumerate(chunks):
            chunks[i] = chunk+"\n"+'%02d of %02d' % (counter, count)
            counter = counter + 1
        self.chunk_list = chunks
        
    def find_Chunks(self,word):
        chunks=[]
        for i in range(1,len(self.chunk_list)):
            findword = finder(r'{0}'.format(word),unicode(self.chunk_list[i]))
            if findword.found():
                chunks.append(self.chunk_list[i])
        if len(chunks) > 0:
            self.chunk_list = chunks
            return True
        else:
            return False
                
    
    def next_Chunk(self):
        self.position+=1; return self
        
    def goto_Chunk(self,number=1):
        if 1 <= number <= len(self.chunk_list)+1:
            self.position = number-1; return self
        else:
            return "Number out of range."

        
    

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
#
#
#
#print map(lambda x:len(x),test.chunk_list)
#print test.find_Chunks('athe')
