# -*- coding: utf-8 -*-
import collections,csv,codecs,operator
from misc import finder,alphabet
from time import time
from places import Directory
from helper import Helper
from options import Options,Chunks
from spacyapi import tokenizer,similarity

global hlp
hlp = Helper()
 
class Main(object):
    def __init__(self,current='main'):
        self.main = Corrector(current)
        self.current = current
        self.previous = current
        self.commands = []
        self.corrected = {}

    def run(self,current='main'):
        
        test = Main();br=True
        while br:
            command = raw_input("SMS in: ");t = test.process(unicode(command))
            words = t[0];disting = t[1][-1]
            for k in range(len(words)):
                dirfin = finder(r'directory|places',words[k])
                if dirfin.found():
                    del words[k];types=[];keywords=[];d=[]
                    test2 = similarity(" ".join(words)," ".join(hlp.dirtypes()),sort=True,average=False)
                    for s in words:
                        for k in test2[s][:4]:
                            if k[1]>=0.5:
                                types.append(k[0])
                                if (s in d) == False:
                                    d.append(s)
                    for i in d:
                        keywords.append(s)
                        del words[words.index(i)]
                    d=[]
                    test4 = similarity(" ".join(words)," ".join(hlp.addresstypes()),average=True)
                            
                    for wo in test4:
                        for keyword in test4[wo]:
                            if keyword[-1]>=0.5:
                                break
                            elif (i in d) == False:
                                d.append(i)
                    for i in d:
                        del words[words.index(i)] 
                    others=disting['numbers']+disting['splits']
                    direc=Directory(words)
                    direc.run(types,keywords,others)
                    print "Back to Main Menu."
                    words = [];break
                      

                exifin = finder(r'exit',words[k])
                if exifin.found():
                    br=False;words=[];break   
                helpfin = finder(r'help',words[k])
                if helpfin.found():
                    print hlp;words=[];break
#                    for j in hlp.list:
#                        if k==j:
#                            detail = j;hlp = Helper(j);print hlp;break
#                            found=True
#                        else found=False
                    
     


    def process(self,command,scope='main'):
        com = Corrector(scope);opts = None;corr=[];com.disting(command)
        for i in com.cur()['words']+com.cur()['splits']:
            for j in com.match(i):
                if j[0]=='None':
                    continue
                if opts == None:
                    opts = Options(heading="By ({0}) Did you mean: ".format(i),
                           footing="Please choose.")
                opts.add_Option(content="{0}".format(j[0]))
            
            if opts:
                ch = opts.select_Option(opts.print_Options())
                if ch == 'exit':
                    return [com.cur()['words'],com.history]
                if ch!=None:
                    corr.append([i,str(opts[ch][1])])
            opts = None
        for k in corr:
            if str(k[1]) in self.corrected:
                self.corrected[str(k[1])].append(k[0])
            else:
                self.corrected[str(k[1])]=[k[0]]
            if k[0] in com.cur()['words']:
                com.cur()['words'][com.cur()['words'].index(k[0])]=str(k[1])
                if k[0] in com.cur()['words']:
                    del com.cur()['words'][com.cur()['words'].index(k[0])]
            elif k[0] in com.cur()['words']==False:
                com.cur()['words'].append(str(k[1]))
                del com.cur()['splits'][com.cur()['splits'].index(k[0])]
            else:
                del com.cur()['splits'][com.cur()['splits'].index(k[0])]
            
        return [com.cur()['words'],com.history]


class Corrector(object):
    def __init__(self,scope='main'):
        self.scope = scope  ## scope must be the same as filename (without .txt)
        self.commands = {"time":["schedule","remind","between", "difference"],
                         "langs":["eng","spa"],
                         "food":[],
                         "main":["exit","time","directory","next","previous",
                         'help','list',"places"],
                         "locations":['london', 'paris', 'sydney', 'san fransisco'],
                         "dirtypes":[]}
        self.commands['dirtypes'] = hlp.dirtypes();self.commands['food'] = hlp.foodtypes()
        self.lang = {"eng":"english","spa":"spanish"}
        self.langsel = "eng"
        self.history = []
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
        if word in self.commands[self.scope]:
            return [("None",10)]
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
            
#    def spellcheck(self,word):
#        d = enchant.Dict("en_US")
#        if d.check(word.lower()) == False:
#            return d.suggest(word.lower())
#        else:
#            return True   
            
#    def correlate()
    

        
          

test3 = Main()
test3.run()



        
