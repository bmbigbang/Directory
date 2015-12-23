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
        self.select = False
        self.lvl=False
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
            self.expand[subs[:-1]]=0
            self.plus = False
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
            
    def output_Outline(self,chap=""):
        strg = "";temp= [];outline=[]
        if self.select:
            for i in self.outline_table:
                if i[0].startswith(chap):
                    outline.append(i)
        else:
            outline = self.outline_table
        for i in range(len(outline)):
            if outline[i][0][:-1] in self.expand:
                if self.expand[outline[i][0][:-1]] == 1:
                    if not self.lvl and outline[i][0].count(".") == self.level:
                        strg = strg+outline[i][0].replace("+","-")+" "+outline[i][1]+"\n" 
                    for j in outline[i+1:]:
                        if self.outline_table[i][0][:-1] in j[0]:
                            if j[0][-1]!="+" and j[0][-1]!="-":
                                temp.append(j[0])
                        else:
                            break
                    continue
                elif not self.lvl and outline[i][0].count(".") == self.level:
                    strg = strg+outline[i][0].replace("-","+")+" "+outline[i][1]+"\n" 
                    continue
            else:
                if self.lvl and outline[i][0].count(".") != self.level:
                    continue
                if outline[i][0] in temp:
                    strg = strg+outline[i][0]+" "+outline[i][1]+"\n"
                    continue
                elif not "." in outline[i][0]:
                    strg = strg+outline[i][0]+" "+outline[i][1]+"\n"

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
        if strg:
            return strg
        else:
            return "Secton not found"
    
    def txt_Check(self,outline):
        for i in range(0,len(self.outline_table)):
            if outline in self.outline_table[i][0]:
                if len(self.outline_table[i][2])>0:
                    return True
        return False
    
table = Outline()
table.delimeter = "\n"
with open("textblock.txt","rb") as f:
    textblock= f.read().decode("string_escape")
    for i in range(len(textblock)):
        if textblock[i:i+2] == "\u":   
            textblock= textblock[:i]+unichr(int(textblock[i+2:i+6],base=16)).encode("utf-8")  +textblock[i+6:]
f.close()
table.add_TxtBlock(textblock); corr = Corrector('outline')
 
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
                              footing="Please choose.")
                print section.goto_Chunk()
                option = raw_input("SMS IN: ")
                if opts.select_Option(option)!=None:
                    t = s.index(i); s[t] = opts[opts.select_Option(option)][2]
                    corr.addHist(i,s[t]); continue
            opts = None
            
    if "tables" in s:
        for p in table.expand:
            table.expand[p] = 0
        section = Chunks(table.output_Outline())
        section.create_Chunks(heading = "Outline Table")              
        print section.goto_Chunk(1) 
        
    if "expand" in s:
        if "all" in s:
            for p in table.expand:
                table.expand[p] = 1
            section = Chunks(table.output_Outline())
            section.create_Chunks(heading = "Outline Table - Expanded All")              
            print section.goto_Chunk(1) 
            continue   
        if len(numbers) > 0 and numbers[0] in table.expand:
            table.expand[numbers[0]] = 1;table.select=True
            section = Chunks(table.output_Outline(chap=numbers[0]))
            section.create_Chunks(heading = "Expanded Chapter {0}".format(numbers[0]))   
            print section.goto_Chunk()
            table.select=False; continue
    
    if "level" in s:   
        for i in numbers:
            if int(i) != 1:
                table.lvl=True
                for p in table.expand:
                    table.expand[p] = 1
            else:
                table.lvl=False
            table.level = int(i)-1
            section = Chunks(table.output_Outline())
            section.create_Chunks(heading = "Level {0} - Outline".format(i),
                                  footing = "Select Outline Number" ) 
            print section.goto_Chunk()
        continue    
        
    for i in numbers:
        if table.lvl==True:
            table.select=True; section = Chunks(table.output_Outline(chap=i))
            section.create_Chunks(heading = "Section {0} - Level {1} Outline".format(i,str(table.level+1)))
            print section.goto_Chunk(); table.lvl=False
        elif table.txt_Check(i):
            table.expand[numbers[0]] = 0
            section = Chunks(table.txt_Item(i))
            section.create_Chunks(heading = "Section {0}".format(i)) 
            print section.goto_Chunk() 
        else:
            table.select=True
            section = Chunks(table.output_Outline(chap=i))
            section.create_Chunks(heading = "Section {0} - Outline".format(i)) 
            print section.goto_Chunk() 
    
    if "exit" in s:
        break
    if "next" in s:
        print section.next_Chunk()

            
            
            
            
            
            
            
            
            
            
            
            
            
            