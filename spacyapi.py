# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 09:22:34 2015

@author: ardavan
"""

import urllib2,json,urllib,operator
  
def tokenizer(sentence):
    base="http://51.255.161.235/api/tokenizer/"
    addressurl = base+ urllib.quote_plus(sentence)
    req = urllib2.Request(addressurl)
    html = urllib2.urlopen(req).read().decode("utf-8")
    data = dict(json.loads(html))
    return data

def similarity(sentence,sen2 = "",sort=False,reverse=True,average=True):
    base="http://51.255.161.235/api/similarity/"; mem = []; mem2 = []
    for i in sentence.split():
        if "_" in i:
            mem.append([i,i.replace("_"," "),i.split("_")])
    for i1 in sen2.split():
        if "_" in i1:
            mem2.append([i1,i1.replace("_"," "),i1.split("_"),sen2.split().index(i1)])
    if sen2:
        sen2 = "&"+sen2
    addressurl = base + urllib.quote_plus(sentence.replace("_"," ")+sen2.replace("_"," "))
    req = urllib2.Request(addressurl)
    html = urllib2.urlopen(req).read().decode("utf-8")
    data = dict(json.loads(html))
    for s in mem:
        temp = [];temp2 = [];temp3 = 0
        for z in range(len(s[2])):
            temp.append(data[s[2][z]])  
        for k1 in range(len(temp[0])):
            for z in range(len(s[2])):
                temp3 +=float(temp[z][k1][1])
            temp2.append([temp[z][k1][0],temp3/len(s[2])])
            temp3 = 0
        data[s[0]] = temp2
    for j in data:
        for s in mem2:
            temp4 = sum([i2[1] for i2 in data[j][s[3]:s[3]+len(s[2])]])/len(s[2])
            data[j].insert(s[3],[s[0],temp4])
            del data[j][s[3]+1:s[3]+len(s[2])+1]
                
        if sort == True:  
            data[j] = sorted(data[j],key=operator.itemgetter(1),reverse=reverse)
        if average == True:
            data[j].append(sum([i3[1] for i3 in data[j]])/len(data[j]))              
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

def filter_Concepts(a,b,c="food"):
    base="http://51.255.161.235/api/filter/"
    addressurl = base + urllib.quote_plus(a + "&" + b + "&" + c)
    req = urllib2.Request(addressurl)
    html = urllib2.urlopen(req).read().decode("utf-8")
    return float(html)
