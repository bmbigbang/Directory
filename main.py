from misc import finder,alphabet
from corrector import Corrector
from time import time
from options import Options,Chunks

class Main(object):
    def __init__(self,current='main'):
        self.main = Corrector(current)
        self.current = current
        self.previous = current
        self.commands = []
    def run(self,current='main'):
        while True:
            command = raw_input("SMS in: ")
            esc = finder(r'^exi',command.lower())
            if esc.found():
                break
            words = self.main.disting(command)
            for i in words['words']:
                if i in self.main.commands[self.main.scope]:
                    self.current = i
                    del words['words'][words['words'].index(i)]
                    time1 = time(words['words'],words['times'])
                    time1.run()


    def process(self,command):
        com = Corrector('main')
        for i in com.disting(command)['words']:
            opts = Options(heading="By ({0}) Did you mean: ".format(i),
                           footing="Please choose.")
            for j in com.match(i):
                if com.match(i)[0][1] <= 3.7:
                    if com.spellcheck(i)==True:
                        opts.add_Option(content="{1}".format(j))
                    else:
                        opts.add_Option(content="{1}".format(j))
                        for k in com.spellcheck(i):
                            opts.add_Option(content="{1}".format(j))
            ch = opts.select_Option(opts)
            com.disting(command)['words'][com.disting(command)['words'].index(i)] = opts[ch][1]
        return com.disting(command)['words']
                


test = Main()
test.process('remi com plete')

            
        
