# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 09:22:34 2015

@author: ardavan
"""
##from spacy.en import .English, .LOCAL_DATA_DIR
##data_dir = os.environ.get('SPACY_DATA',LOCAL_DATA_DIR)
##nlp = English(data_dir=data_dir,tagger = True,entity=True)
inp = raw_input("SMS in: ")
doc = nlp(unicode(inp))
for tokens in doc:
    for ents in tokens.ents:
        print ents.label_ +", " +ents.string +", "+tokens.idx
nlp = English(data_dir=data_dir)
doc = nlp(unicode("remind me 12th dec morning"))
print doc[0]
        

        
        
    