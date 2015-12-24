# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 10:52:12 2015

@author: ardavan
"""
from options import Chunks

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
        
    def run(self,s,numbers):

        if "tables" in s:
            for p in self.expand:
                self.expand[p] = 0
            section = Chunks(self.output_Outline())
            section.create_Chunks(heading = "Outline Table") 
            return section
        
        if "expand" in s:
            if "all" in s:
                for p in self.expand:
                    self.expand[p] = 1
                section = Chunks(self.output_Outline())
                section.create_Chunks(heading = "Outline Table - Expanded All")              
                return section
                
            if len(numbers) > 0 and numbers[0] in self.expand:
                self.expand[numbers[0]] = 1;self.select=True
                section = Chunks(self.output_Outline(chap=numbers[0]))
                section.create_Chunks(heading = "Expanded Chapter {0}".format(numbers[0])) 
                self.select=False; return section
        
        if "level" in s:   
            for i in numbers:
                if int(i) != 1:
                    self.lvl=True
                    for p in self.expand:
                        self.expand[p] = 1
                else:
                    self.lvl=False
                self.level = int(i)-1
                section = Chunks(self.output_Outline())
                section.create_Chunks(heading = "Level {0} - Outline".format(i),
                                      footing = "Select Outline Number" ) 
                return section
            
        for i in numbers:
            if self.lvl==True:
                self.select=True; section = Chunks(self.output_Outline(chap=i))
                section.create_Chunks(heading = "Section {0} - Level {1} Outline".format(i,str(self.level+1)))
                self.lvl=False; return section
            elif self.txt_Check(i):
                self.expand[numbers[0]] = 0
                section = Chunks(self.txt_Item(i))
                section.create_Chunks(heading = "Section {0}".format(i)) 
                return section
            else:
                self.select=True
                section = Chunks(self.output_Outline(chap=i))
                section.create_Chunks(heading = "Section {0} - Outline".format(i)) 
                return section
        return False

            
            
            
            
            
            
            
            
            
            
            
            
            
            