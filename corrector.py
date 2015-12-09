# -*- coding: utf-8 -*-
import collections,re,csv,codecs,operator,enchant
from misc import finder,alphabet
import os, numpy, spacy
from spacy.en import English, LOCAL_DATA_DIR
data_dir = os.environ.get('SPACY_DATA',LOCAL_DATA_DIR)
try:
    assert nlp != None
except:
    nlp = English(data_dir=data_dir) 

entitymap = {'PERSON':'People, including fictional.',
             'NORP':'Nationalities or religious or political groups.',
             'FACILITY':'Buildings, airports, highways, bridges, etc.',
             'ORG':'Companies, agencies, institutions, etc.',
             'GPE':'Countries, cities, states.',
             'LOC':'Non-GPE locations, mountain ranges, bodies of water.',
             'PRODUCT':'Vehicles, weapons, foods, etc. (Not services)',
            'EVENT':'Named hurricanes, battles, wars, sports events, etc.',
            'WORK_OF_ART':'	Titles of books, songs, etc.',
            'LAW':'Named documents made into laws',
            'LANGUAGE':'Any named language',
            'DATE':'Absolute or relative dates or periods',
            'TIME':'Times smaller than a day',
            'PERCENT':'Percentage (including %)',
            'MONEY':'Monetary values, including unit',
            'QUANTITY':'Measurements, as of weight or distance',
            'ORDINAL':'first", "second"',
            'CARDINAL':'Numerals that do not fall under another type'}

class Corrector:
    
    def __init__(self,scope):
        self.scope = scope  ## scope must be the same as filename (without .txt)
        self.commands = {"time":["schedule","remind","between", "difference"],
                         "langs":["eng","spa"],
                         "food":["italian","pizza","bacon","mexican","chinese",
                         "vegetarian","lebanese","indian"],
                         "main":["exit","time","directory","next","previous",'list'],
                         "locations":['london', 'paris', 'sydney', 'san fransisco'],
                         "dirtypes":['accounting','airport','amusement_park',
                         'aquarium','art_gallery','atm','bakery',
'bank','bar','beauty_salon','bicycle_store','book_store','bowling_alley',
'bus_station','cafe','campground','car_dealer','car_rental','car_repair',
'car_wash','casino','cemetery','church','city_hall','clothing_store',
'convenience_store','courthouse','dentist','department_store','doctor',
'electrician','electronics_store','embassy','establishment','finance',
'fire_station','florist','food','funeral_home','furniture_store',
'gas_station','general_contractor','grocery_or_supermarket','gym',
'hair_care','hardware_store','health','hindu_temple','home_goods_store',
'hospital','insurance_agency','jewelry_store','laundry','lawyer','library',
'liquor_store','local_government_office','locksmith','lodging','meal_delivery',
'meal_takeaway','mosque','movie_rental','movie_theater','moving_company',
'museum','night_club','painter','park','parking','pet_store','pharmacy',
'physiotherapist','place_of_worship','plumber','police','post_office',
'real_estate_agency','restaurant','roofing_contractor','rv_park','school',
'shoe_store','shopping_mall','spa','stadium','storage','store',
'subway_station','synagogue','taxi_stand','train_station','travel_agency',
'university','veterinary_care','zoo']}
        self.lang = {"eng":"english","spa":"spanish"}
        self.langsel = "eng"
        self.history = []

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
        return dicfin

    def hashtable(self):
        temp=[]
        for i in self.commands[self.scope]:
            temp2=collections.Counter(dict(collections.Counter(i.lower()).most_common()))
            temp.append([i.lower(),temp2])
        return temp
    
    def match(self,word):
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
            if results[i] >= 4:
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
                
            if results[i] >= 8 and (i in rem)==False:
                rem.append(i)  

        for i in rem:
            del results[i]
                        
        resultsorted = sorted(results.items(),key=operator.itemgetter(1))
        if len(resultsorted)==0:
            return [("None",10)]
        else:
            return resultsorted

    def similarity(self,sentence,sen2 = ""):
        res={}; doc = nlp(unicode(sentence))
        if len(sen2)==0:
            doc2 = nlp(unicode(sentence))
        else:
            doc2 = nlp(unicode(sen2))
        
        for i in doc:
            for j in doc2:
                if str(i) != str(j) and str(i.pos_)!='PUNCT' and str(j.pos_)!='PUNCT':
                    if str(i.pos_)!='NUM' and str(j.pos_)!='NUM':
                        if str(i.orth_) in res:
                            res[str(i.orth_)].append([str(j.orth_),i.similarity(j)])
                        else:
                            res[str(i.orth_)]=[[str(j.orth_),i.similarity(j)]]
        for i in res:
            res[i]=sorted(res[i],key=operator.itemgetter(1),reverse=True)
            res[i].append(sum([j[1] for j in res[i]])/len(res[i]))
        return res
    
    def lemma(self,sentence):
        res=[]; doc = nlp(unicode(sentence))
        for token in doc:
            try:
                res.append([token.orth_,token.lemma_])
            except:
                res.append([token.orth_,""])
        return res
        
    def spellcheck(self,word):
        d = enchant.Dict("en_US")
        if d.check(word.lower()) == False:
            return d.suggest(word.lower())
        else:
            return True
        
    
            

     
        
#### test daacollect function
##test = Corrector('locations')
##print(test.commands[test.scope])
##test.datacollect(test.scope,test.commands)
##print(test.commands[test.scope])
##print "please choose scopes: #locations or #time"
##
##test = Corrector('food')
##
##while True:
##    command = raw_input("SMS in: ")
##    comloc = finder(r'^#l',command.lower())
##    comtim = finder(r'^#t',command.lower())
##    esc = finder(r'^exi',command.lower())
##    langs = finder(r'^lang',command.lower())
##
##    
##    
##    if esc.found():
##        break
##    
##    if comloc.found():
##        test.scope=('locations')
##        test.datacollect(test.scope,test.commands)
##        continue
##    
##    elif comtim.found():
##        test.scope=('time')
##        continue
##
##    if langs.found():
##        test.scope=('langs')
##        for j in test.commands['langs']:
##            langfinder = finder(j,command.lower())
##            if langfinder.found():
##                test.langsel=j
##                break
##            
##        if langfinder.found()==False:        
##            print "language not found"
##        continue
##                
##        
##    print test.disting(command)
##    for i in test.disting(command)['words']:
##        print test.match(i)[0]

##print test.similarity('london')
##print test.similarity('english')
##print test.similarity('pizza')
##print test.similarity('vegetarian')
##print u'{0}'.format(test.alphabet())
##    words = test.disting(command)
##    print(words)
    
#test = Corrector('time')
#resu={};inp="london burger"
#for j in test.commands['dirtypes']:
#    test2 = test.similarity(inp,j.replace('_',' '))
#    for k in inp.split():
#        if k in resu:
#            resu[k].append([j,test2[k][-1]])
#        else:
#            resu[k]= [[j,test2[k][-1]]]
#
#k = sorted(resu['london'],key=operator.itemgetter(1),reverse=True)
#print k




