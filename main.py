# -*- coding: utf-8 -*-
import collections,re,csv,codecs,operator,enchant
from misc import finder,alphabet
from time import time
from places import Directory
from helper import Helper
from options import Options,Chunks
import os,numpy,spacy
from spacy.en import English, LOCAL_DATA_DIR
data_dir = os.environ.get('SPACY_DATA',LOCAL_DATA_DIR)
try:
    aeghaehtaeh = nlp(unicode('s'))
except:
    nlp = English(data_dir=data_dir)
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
            command = raw_input("SMS in: ");t = test.process(command)
            words = t[0];disting = t[1][-1]
            for k in range(len(words)):
                dirfin = finder(r'directory|places',words[k])
                if dirfin.found():
                    del words[k];resu={};types=[];resu2={};keywords=[];d=[]
                    for j in hlp.dirtypes():
                        test2 = similarity(words,j.replace('_',' '))

                        for s in words:
                            if len(test2)==0:
                                break
                            if s in resu:
                                resu[s].append([j,test2[s][-1]])
                            else:
                                resu[s]= [[j,test2[s][-1]]]
                    for h in words:
                        if h in resu:
                            resu[h] = sorted(resu[h],key=operator.itemgetter(1),reverse=True)
                            resu[h] = resu[h][:4]
                    for wo in resu:
                        for dirtypes in resu[wo]:
                            if dirtypes[1]>=0.5:
                                types.append([dirtypes[0],dirtypes[1]])
                                  
                                for i in range(len(words)):
                                    if words[i] == wo:
                                        if (i in d) == False:
                                            d.append(i)
                    
                    for i in d:
                        keywords.append(words[i])
                        del words[i]
                    d=[]
                    
                    for j in hlp.addresstypes():
                        test4 = similarity(words,j)

                        for s in words:
                            if len(test4)==0:
                                break
                            if s in resu2:
                                resu2[s].append([j,test4[s][-1]])
                            else:
                                resu2[s] = [[j,test4[s][-1]]]
                               
                    for h in words:
                        if h in resu2:
                            resu2[h] = sorted(resu2[h],key=operator.itemgetter(1),reverse=True)
                            resu2[h] = resu2[h][:5]
                            
                    for wo in resu2:
                        for keyword in resu2[wo]:
                            if keyword[1]>=0.5:
                                break
                            for i in range(len(words)):
                                if words[i] == wo:
                                    if (i in d) == False:
                                        d.append(i)
                                            
                    for i in d:
                        del words[i]      
                        
                    others=disting['numbers']+disting['splits']
                    direc=Directory(words)
                    direc.run(resu,resu2,types,keywords,others)
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
                    return com.cur()['words']
                if ch!=None:
                    corr.append([i,str(opts[ch][2])])
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
        
        tokenizer = [];entities=[];types={};doc = nlp(unicode(text))
        for token in doc:
            tokenizer.append(str(token.orth_))
            if str(token.pos_) in types:
                types[token.pos_].append(str(token.orth_))
            else:
                types[token.pos_]=[str(token.orth_)]
        for ents in doc.ents:
            entities.append([str(ents.orth_),str(ents.label_)])
            
        dicfin = {'tokens':tokenizer,'entities':entities,'types':types,
                  'words':[],'times':[],'numbers':[],'splits':[]}
        
        for i in tokenizer:
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
            
    def spellcheck(self,word):
        d = enchant.Dict("en_US")
        if d.check(word.lower()) == False:
            return d.suggest(word.lower())
        else:
            return True   

def similarity(sentence,sen2 = ""):
    res={}; doc = nlp(unicode(sentence))
    if len(sen2)==0:
        doc2 = nlp(unicode(sentence))
    else:
        doc2 = nlp(unicode(sen2))
    
    for i in doc:
        for j in doc2:
            if str(i.pos_)!='PUNCT' and str(j.pos_)!='PUNCT':
                if str(i.pos_)!='NUM' and str(j.pos_)!='NUM':
                    if str(i.orth_) in res:
                        res[str(i.orth_)].append([str(j.orth_),i.similarity(j)])
                    else:
                        res[str(i.orth_)]=[[str(j.orth_),i.similarity(j)]]
    for i in res:
        res[i]=sorted(res[i],key=operator.itemgetter(1),reverse=True)
        res[i].append(sum([j[1] for j in res[i]])/len(res[i]))
    return res
    
#    def correlate()
    
def lemma(sentence):
    res=[]; doc = nlp(unicode(sentence))
    for token in doc:
        try:
            res.append([token.orth_,token.lemma_])
        except:
            res.append([token.orth_,""])
    return res
        

            
            


test3 = Main()
test3.run()



        
