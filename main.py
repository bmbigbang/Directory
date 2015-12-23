# -*- coding: utf-8 -*-

from misc import finder,alphabet
from places import Directory
from helper import Helper
from options import Options,Chunks
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
            if "find" in words:
                del disting['tokens'][disting['tokens'].index("find")]
                display.create_Chunks(heading="Find {0}".format(" ".join(disting['tokens'])))
                expand = display.find_Chunks(" ".join(disting['tokens']))
                if expand:
                    print display.goto_Chunk()
                else:
                    print "No results found"
                continue
            
            for k in range(len(words)):
                dirfin = finder(r'directory|places',words[k])   
                if dirfin.found():
                    del words[k]
                    if "list" in words:
                        print ""
                        display = Chunks(",".join(hlp.dirtypes()).replace("_"," "))
                        display.create_Chunks(heading="List of types of places:")
                        print display.goto_Chunk()
                        break
                    direc=Directory(words)
                    results,resultsort = direc.run(disting)
                    if results == None:
                        words=[];break
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
                
                if "next" in words[k]:
                    print display.next_Chunk(); break
                
                if "goto" in words[k]:
                    try:
                        n = disting['numbers'][0]
                        num = int(n)
                    except:
                        num = 1000
                    print display.goto_Chunk(num); break
                    
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
                        k = com.cur()['words'].index(i)
                        com.cur()['words'][k] = j[0]
                    except:
                        com.cur()['words'].append(j[0])
                    continue
                        
                if j[0] == "find":
                    return [com.cur()['words'],com.history]
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
                        k = com.cur()['words'].index(i)
                        com.cur()['words'][k] = j[0]
                    except:
                        com.cur()['words'].append(j[0])
                    if opts[opts.select_Option(option)][2] == "find":
                        return [com.cur()['words'],com.history]
            opts = None
            
        return [com.cur()['words'],com.history] 
        
test3 = Main()
test3.run()





        
