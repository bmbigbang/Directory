# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 09:22:34 2015

@author: ardavan
"""

import urllib2,json,urllib
  
def tokenizer(sentence):
    base="http://51.255.161.235/api/tokenizer/"
    addressurl = base+ urllib.quote_plus(sentence)
    req = urllib2.Request(addressurl)
    html = urllib2.urlopen(req).read().decode("utf-8")
    data = dict(json.loads(html))
    return data

def similarity(sentence,sen2 = ""):
    base="http://51.255.161.235/api/similarity/"
    if sen2:
        sen2 = "&"+sen2
    addressurl = base + urllib.quote_plus(sentence+sen2)
    req = urllib2.Request(addressurl)
    html = urllib2.urlopen(req).read().decode("utf-8")
    data = dict(json.loads(html))
    return data

def lemma(sentence):
    base="http://51.255.161.235/api/lemma/"
    addressurl = base + urllib.quote_plus(sentence)
    req = urllib2.Request(addressurl)
    html = urllib2.urlopen(req).read().decode("utf-8")
    data = json.loads(html)
    return data
    
def vector(sentence):
    base="http://51.255.161.235/api/vector/"
    addressurl = base + urllib.quote_plus(sentence)
    req = urllib2.Request(addressurl)
    html = urllib2.urlopen(req).read().decode("utf-8")
    data = json.loads(html)
    for k in data:
        for i in range(len(data[k])):
            data[k][i] = float(data[k][i])            
    return data

def filter_Concepts(a,b,c):
    base="http://51.255.161.235/api/filter/"
    addressurl = base + urllib.quote_plus(a + "&" + b + "&" + c)
    req = urllib2.Request(addressurl)
    html = urllib2.urlopen(req).read().decode("utf-8")
    return html

#doc = "food pizza pasta chinese weather"
#docv = vector(doc)      
#i= filterConcepts(docv["food"],docv["chinese"])    
#j= numpy.convolve(docv["food"],docv["chinese"],mode="same")   
#print numpy.inner(i[0],docv["pizza"])," - pizza to chinese through food"
#print numpy.inner(i[0],docv["weather"])," - weather to pizza through food"
#print numpy.inner(j,docv["pizza"])," - pizza to chinese through food"
#print numpy.inner(j,docv["weather"])," - weather to chinese through food"
#print numpy.inner(docv["food"],docv["chinese"])," - food to chinese"
#print numpy.inner(docv["pizza"],docv["chinese"])," - pizza to chinese"



            
        
            
            
            
        
        
    