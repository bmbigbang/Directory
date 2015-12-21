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
        hlp = Helper();br=True
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
                    direc.run(types,keywords,others)
                    print "Back to Main Menu."
                    words = [];break
                      

                exifin = finder(r'exit',words[k])
                if exifin.found():
                    br=False;words=[];break   
                helpfin = finder(r'help',words[k])
                if helpfin.found():
                    print hlp;words=[];break
                    

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
        
test3 = Main()
test3.run()





        
