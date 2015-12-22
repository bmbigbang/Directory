# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 16:17:56 2015

@author: ardavan
"""
from spacyapi import tokenizer
import collections,csv,operator
from misc import finder,alphabet
from helper import Helper
hlp = Helper()

class Corrector(object):
    def __init__(self,scope='main',history={}):
        self.scope = scope  ## scope must be the same as filename (without .txt)
        self.commands = {"time":["schedule","remind","between", "difference"],
                         "langs":["eng","spa"],
                         "food":[],
                         "main":["exit","time","directory","next","previous",
                         'help','list',"places"],
                         "locations":['london', 'paris', 'sydney', 'san fransisco'],
                         "dirtypes":[],
                         "outline":["exit","next","expand","tables","goto","level",
                         "help", "all","find"]}
        self.commands['dirtypes'] = hlp.dirtypes();self.commands['food'] = hlp.foodtypes()
        self.lang = {"eng":"english","spa":"spanish"}
        self.langsel = "eng"
        self.history = []
        self.correctedHistory = history
        self.current = {}
    
    def cur(self):
        return self.current

    def datacollect(self,filename,setdir):
        with open(filename+".txt",'r') as csvfile:
            csvreader = csv.reader(csvfile,delimiter=",")

            for row in csvreader:
                try:
                    setdir[filename].append(row[1])
                except UnicodeEncodeError:
                    print("error with encoding:"+row[1])
                    continue

    def disting(self,text):
        
        sptok = tokenizer(text);tokens = sptok['tokens']
        entities= sptok['entities']; types=sptok['types']
        dicfin = {'tokens':tokens,'entities':entities,'types':types,
                  'words':[],'times':[],'numbers':[],'splits':[]}
        for i in tokens:
            timefinder = finder(r'[-|/|:|@|\\]',i)
            if timefinder.found():
                dicfin['times'].append(i)
            wordfinder = finder(r'\w+',i)
            numberfinder = finder(r'\d+',i)
            symbolfinder = finder(r',|\.',i)
            timefinder2 = finder(r'\d(th|st|rd)',i.lower())

            if wordfinder.found() and numberfinder.found():
                if timefinder2.found():
                    dicfin['times'].append(i)
                elif len(wordfinder.result())!=len(numberfinder.result()):
                    dicfin['splits'].append(i)
            if numberfinder.found() and symbolfinder.found():
                dicfin['numbers'].append(i)
            if numberfinder.found() and (timefinder.found()==False) and (timefinder2.found()==False):
                if (i in dicfin['splits']) is False and (symbolfinder.found()==False):
                    dicfin['numbers'].append(i)
            if wordfinder.found() and (numberfinder.found()==False) and (symbolfinder.found()==False):
                dicfin['words'].append(i)
        self.history.append(dicfin)
        self.current = dicfin

    def hashtable(self):
        temp=[]
        for i in self.commands[self.scope]:
            temp2=collections.Counter(dict(collections.Counter(i.lower()).most_common()))
            temp.append([i.lower(),temp2])
        return temp
    
    def match(self,word):
        if word in self.commands[self.scope] or len(word)==1:
            return [("None",10)]
        if self.matchHist(word) != None:
            return[(self.matchHist(word),0)]
        hashtable = self.hashtable();results={}
        wordc=collections.Counter(dict(collections.Counter(word.lower()).most_common()))
        ab = alphabet(self.lang[self.langsel]);abcd = ab.retstr()
        
        for i in wordc:
            for j in hashtable:
                if j[0] in results and results[j[0]] >= 4:
                    continue
                if i in j[1]:
                    if j[0] in results:
                        results[j[0]]+=abs(int(wordc[i])-int(j[1][i]))
                    else:
                        results[j[0]]=abs(int(wordc[i])-int(j[1][i]))
                else:
                    if j[0] in results:
                        results[j[0]]+=int(wordc[i])
                    else:
                        results[j[0]]=int(wordc[i])
        rem = []
        for i in results:
            results[i]+=abs(1.0-((len(word)*1.0)/len(i)))
        
        for i in results:
            if results[i] >= 3.33:
                rem.append(i)
 
            else:
                for j in hashtable:
                    if j[0] == i:
                        for z in j[1]:
                            if z in wordc:
                                continue
                            else:
                                results[i]+=int(j[1][z])

        for i in results:
            for k in range(len(i)):
                try:
                    if i[k] != word[k]:
                        results[i]+=1
                except:
                    pass
                
            if results[i] >= 7 and (i in rem)==False:
                rem.append(i)  

        for i in rem:
            del results[i]
                        
        resultsorted = sorted(results.items(),key=operator.itemgetter(1))
        if len(resultsorted)==0:
            return [("None",10)]
        else:
            return resultsorted
    
    def addHist(self,word,final):
        self.correctedHistory[word] = final
            
    def matchHist(self,word):
        if word in self.correctedHistory:
            return self.correctedHistory[word]
        else:
            return None 
            
                
#    def spellcheck(self,word):
#        d = enchant.Dict("en_US")
#        if d.check(word.lower()) == False:
#            return d.suggest(word.lower())
#        else:
#            return True   
            
