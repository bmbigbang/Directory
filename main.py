# -*- coding: utf-8 -*-

from misc import finder,alphabet
from places import Directory
from helper import Helper
from options import Options,Chunks
from spacyapi import similarity
from corrector import Corrector
 
class Main(object):
    def __init__(self,current='main'):
        self.main = Corrector(current)
        self.current = current
        self.previous = current
        self.commands = []
        self.corrected = {}

    def run(self,current='main'):
        hlp = Helper();br=True;display=Chunks("");display.create_Chunks()
        results={};resultsort=[];option = Options()
        while br:   
            command = raw_input("SMS in: ");t = self.process(unicode(command))
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
                    results,resultsort = direc.run(types,keywords,others)
                    for i in resultsort:
                        option.add_Option(content="{0} - Ratings : {1}".format(i[0].encode('utf-8'),str(i[1])))
                    display = Chunks(option.print_Options())
                    display.create_Chunks(heading="Available places found nearby:",
                              footing="Please choose an option. ")
                    print display.goto_Chunk()
                    words = [];break
                
                exifin = finder(r'exit',words[k])
                if exifin.found():
                    br=False;words=[];break   
                helpfin = finder(r'help',words[k])
                if helpfin.found():
                    print hlp;words=[];break    
                
                print display.chunk_list
                if "next" in words[k]:
                    print display.next_Chunk(); break
                
                if "find" in words[k]:
                    try:
                        del words[k]
                        display.create_Chunks(heading="Find {0}".format(" ".join(words),
                                  footing = "Select Outline Number" ))
                        expand = display.find_Chunks(" ".join(words))
                        if expand:
                            print display.goto_Chunk(expand[0])
                        else:
                            print "No results found"
                    except:
                        pass
                    
                if len(option)>0 and len(words[k])==1:
                    ch = option.select_Option(words[k])
                    if ch!=None:
                        text = "{0} - Ratings : {1}".format(resultsort[ch][0],resultsort[ch][1])
                        text += "\n" +" Telephone Number: " + results[resultsort[ch][0]][1]
                        text += "\n Address: "+results[resultsort[ch][0]][0]
                        display = Chunks(text)
                        display.create_Chunks()
                        print display.goto_Chunk()
                        option = Options()

    def process(self,command,scope='main'):
        com = Corrector(scope,history=self.corrected);opts = None;com.disting(command)
        for i in com.cur()['words']+com.cur()['splits']:
            for j in com.match(i):
                if j[0]=='None':
                    continue
                if j[1]==0:
                    try:
                        t = com.cur()['words'].index(i)
                        com.cur()['words'][t] = j[0]
                    except:
                        t = com.cur()['splits'].index(i)
                        com.cur()['words'].append(j[0])
                    continue
                if opts == None:
                    opts = Options()
                opts.add_Option(content="{0}".format(j[0]))
            
            if opts:
                select = Chunks(opts.print_Options())
                select.create_Chunks(heading="By ({0}) Did you mean: ".format(i),
                           footing="Please choose.")
                print select.goto_Chunk()
                option = raw_input("SMS in: ")
                if option == 'exit':
                    return [com.cur()['words'],com.history]
                if opts.select_Option(option)!=None:
                    self.corrected[i]=opts[opts.select_Option(option)][2]
                    try:
                        t = com.cur()['words'].index(i)
                        com.cur()['words'][t] = j[0]
                    except:
                        t = com.cur()['splits'].index(i)
                        com.cur()['words'].append(j[0])
                    continue
            opts = None
            
        return [com.cur()['words'],com.history] 
        
test3 = Main()
test3.run()





        
