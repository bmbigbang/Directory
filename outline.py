# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 10:52:12 2015

@author: ardavan
"""
from corrector import Corrector
from options import Options,Chunks
from misc import finder

class Outline(str):
    def __init__(self):
        self.outline_table = []
        self.levels = {'levels':[0,0,0,0,0,0,0,0,0]}
        self.expand = {}
        self.level = 0
        self.set_Level = 0
        self.position = 0
        self.heading = ""
        self.footing = "" 
        self.plus = False
    
    def add_Section(self,title="",content=""):
        self.levels['levels'][self.level] +=1
        for i in range(self.level+1,len(self.levels['levels'])):
            self.levels['levels'][i]=0
        subs = str(self.levels['levels'][0])
        for i in range(1,self.level+1):
            subs = subs+"."+str(self.levels['levels'][i])
        if self.plus:
            subs=subs+"+"
            self.expand[subs[:-1]]=1
            self.plus = False
        else:
        line = [subs,title,content]
        self.outline_table.append(line)
        self.levels[subs] = self.levels['levels']
        
    def add_TxtBlock(self,textblock):
        ## anything between 2 pairs of equal signs is a section title
        ## anything between 1 pair of equal signs is a subsection
        ## " Edit" is to be deleted string
        connectors = ["and","or","of","for","a"]
        title = "";content = ""; lines_raw = textblock.split("\n");lines = filter(None,lines_raw)
        for i, line in enumerate(lines):
            strg = lines[i].lstrip();step = 0
            if 0==strg.find("=="):  ## title found
                
                for j in strg:
                    if j=="=":
                        step += 1
                    else:
                        break
                strg = strg.replace("=","")
                strg = strg.replace("Edit ","").strip()
                if self.level < (step - 2) and title:
                    self.plus=True
                else:
                    self.plus=False
                if title:
                    self.add_Section(title,content)
                    title = ""
                    content = ""
                self.level = step - 2
                title_words = strg.split(" ")
                for k, word in enumerate(title_words):
                    if not title_words[k] in connectors:
                        title_words[k] = word.capitalize()
                title = " ".join(title_words)
            else:   ## title not found
                content +=strg
        if title:
            self.add_Section(title,content)
            
    def output_Outline(self,outline="",lvl=False):
        strg = ""
        if self.heading:
            strg = self.heading+"\n"
        if not outline:
            for i in range(0,len(self.outline_table)):
                linelevel=self.outline_table[i][0].count(".")
                if self.outline_table[i][0][:-1] in self.expand:
                    if self.expand[self.outline_table[i][0][:-1]] == 1:
                        if "." in self.outline_table[i][0]:
                            continue
                if lvl and self.outline_table[i][0].count(".") != self.level:
                    continue
                if self.outline_table[i][0][:-1] in self.expand:
                    if self.expand[self.outline_table[i][0][:-1]]==1:
                        strg = strg+self.outline_table[i][0].replace("-","+")+" "+self.outline_table[i][1]+"\n"
                elif self.outline_table[i][0][0] in [s[0] for s in self.expand]:
                    strg = strg+self.outline_table[i][0].replace("+","-")+" "+self.outline_table[i][1]+"\n"
        else:
            strg += self.outline_table[self.outline_table.index(outline[0])-1][1] + "\n"
            for i in range(0,len(outline)):
                strg = strg+outline[i][0]+" "+outline[i][1]+"\n"
        if self.footing:
            strg = strg+self.footing+"\n"
        if len(strg)==0:
            return "No items found"
        return strg  
        
    def exp_col(self,outline):
        if self.expand[outline]==1:
            self.expand[outline]=0
            for i in range(len(self.outline_table)):
                if self.outline_table[i][0][0]==outline:
                    break
        else:
            self.expand[outline]=1
            for i in range(len(self.outline_table)):
                if self.outline_table[i][0][0]==outline:
                    break
    def txt_Item(self,outline):
        strg = ""
        for section in enumerate(self.outline_table):
            if section[1][0].replace("+","").replace("-","")==outline:
                strg = strg+section[1][0]+" "+section[1][1]+"\n"
                strg = strg+section[1][2]+"\n"
                break
        return strg
    
table = Outline()
table.delimeter = "\n"
with open("textblock.txt","rb") as f:
    textblock= f.read().decode("string_escape")
    for i in range(len(textblock)):
        if textblock[i:i+2] == "\u":   
            textblock= textblock[:i]+unichr(int(textblock[i+2:i+6],base=16)).encode("utf-8")  +textblock[i+6:]
f.close()
table.add_TxtBlock(textblock); corr = Corrector('outline')
print table.expand
    
while 1:
    sms_in = raw_input("SMS IN: ").lower()
    
    opts = None;s= sms_in.split(); numbers = [];temp=[]

    for i in sms_in.split():
        dig = finder(r'\.',i); num = finder(r'^\d',i)
        if dig.found():
            numbers.append(i);del s[s.index(i)]
            continue
        elif num.found():
            numbers.append(i);del s[s.index(i)]
            continue
        for j in corr.match(i):
            if j[0]=='None':
                continue
            if j[1]==0:
                t = s.index(i)
                s[t]=j[0]
                continue
            if opts == None:
                opts = Options()
            opts.add_Option(content="{0}".format(j[0]))
        
            if opts:
                section = Chunks(opts.print_Options())
                section.create_Chunks(heading="By ({0}) Did you mean: ".format(i),
                              footing="Please choose.");z=0
                print section.goto_Chunk()
                option = raw_input("SMS IN: ")
                print opts
                if opts.select_Option(option)!=None:
                    t = s.index(i)
                    
                    s[t] = opts[opts.select_Option(option)][2]
                    corr.addHist(i,s[t])
                    continue
            opts = None
    if "tables" in s:
        section = Chunks(table.output_Outline())
        section.create_Chunks(heading = "Outline",
                              footing = "Select Outline Number" )              
        print section.goto_Chunk(1) 
        
    if "expand" in s:
        if len(numbers)>0 and len(numbers[0])==1:
            table.exp_col(numbers[0])
            section = Chunks(table.output_Outline())
            section.create_Chunks(heading = "Outline",
                                  footing = "Select Outline Number" )              
            print section.goto_Chunk(1) 
        if "all" in s:
            for p in table.expand:
                table.exp_col(p)
            section = Chunks(table.output_Outline())
            section.create_Chunks(heading = "Outline",
                                  footing = "Select Outline Number" )              
            print section.goto_Chunk(1) 
        
        continue        
                   
    if "find" in s:
        del s[s.index("find")]
        newtable = table.find_Outline(" ".join(s))
        section = Chunks(table.output_Outline(newtable))
        section.create_Chunks(heading="Find {0}".format(" ".join(s)),
                              footing = "Select Outline Number" ) 
        print section.goto_Chunk(1) 
        continue
    
    if "exit" in s:
        break 
    
    if "next" in s:
        print section.next_Chunk()
        continue
            
    if "goto" in s:
        n = sms_in.split(" ")
        try:
            num = int(n[1])
        except:
            num = 1000
        print section.goto_Chunk(num)  
        continue
    
    if "level" in s:   
        for i in numbers:
            if int(i) != 1:
                for p in range(len(table.expand)):
                    table.expand[p] = 0
            table.level = int(i)-1;table.set_Level = 1
            section = Chunks(table.output_Outline(lvl=True))
            section.create_Chunks(heading = "Level {0} - Outline".format(i),
                                  footing = "Select Outline Number" ) 
            print section.goto_Chunk(1) 
            for p in table.expand:
                    table.expand[p] = 1
        if table.level==0:
            table.set_Level = 0
        if len(sms_in.split())==1 and table.set_Level == 1:
            print "Level disabled";table.set_Level == 0;table.level=0
        continue    
        
    for i in numbers:
        if table.set_Level == 1:
            for p in range(len(table.expand)):
                table.expand[p]=1
            if len(i)==1:
                tst = [];tst2=[]
                for asd in range(len(table.outline_table)):
                    if int(table.outline_table[asd][0][0])==int(i) and table.outline_table[asd][0].count(".")==table.level:
                        tst.append(asd)
                for asd2 in tst:
                    tst2.append(table.outline_table[asd2])
                if len(tst2) == 0:
                    print "Section Empty"
                    break
                section.create_Chunks(table.output_Outline(tst2),
    heading = "Level {0} - Section {1} - Outline".format(str(table.level+1),i),
                                  footing = "Select Outline Number" ) 
                print section.goto_Chunk(1) 
            break
        for j in range(len(table.outline_table)):
            if i in table.outline_table[j][0]:
                if table.outline_table[j][2] == "":
                    section = Chunks(table.output_Outline(table.outline_table[j+1:]))
                    section.create_Chunks(heading = "Section Empty - Outline",
                                          footing = "Select Outline Number" ) 
                    print section.goto_Chunk(1) 
                    break
                else:
                    section = Chunks(table.txt_Item(i))
                    section.create_Chunks()
                    print section.goto_Chunk(1)
                    break
        continue
                    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            