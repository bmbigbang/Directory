# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 09:22:34 2015
@author: ardavan
"""
import json,urllib2,operator,re,urllib
from options import Options,Chunks
from misc import finder,alphabet
from helper import Helper
from spacyapi import similarity,filter_Concepts


class Directory(object):
    def __init__(self,args):
        self.args = args
        self.locs = []
        self.history = {}

    def run(self, disting, his):
        types = []
        keywords = []
        d=["places"]
        hlp = Helper()
        self.history = his
        add = []
        test2 = similarity(" ".join(self.args), " ".join(hlp.dirtypes()),
                           sort=True, average=False)

        for s in self.args:
            for k in test2[s][:4]:
                if k[1] >= 0.5:
                    types.append(k[0])
                    if s not in d:
                        d.append(s)
        test4 = similarity(" ".join([i for i in self.args if i not in d]),
                           " ".join(hlp.addresstypes()), sort=False, average=True)
        for wo in test4:
            if test4[wo][-1] <= 0.4:
                continue
            elif wo not in add and wo in self.args:
                add.append(wo)
        p = []
        if "food" in types and len([i for i in self.args if i not in (d + add)]) >= 1:
            for j in [i for i in self.args if i not in (d + add)]:
                for k in d[1:]:
                    if filter_Concepts(k, j) > 4000 and j not in p:
                        p.append(j)
        d += p

        others = disting['numbers']+disting['splits']
        found, index = self.check_location(" ".join([i for i in self.args if i not in d] + others))
        if found:
            self.locs = self.history[index]
        types = "&types=" + "|".join(types)
        keywords= "&keyword=" + "+".join(keywords + d[1:])
        address = "address=" + "+".join([i for i in self.args if i not in d+add] + others + add)
        key="&key=AIzaSyAgcnAoMCuhgMwXLXwRuGiEZmP0T-oWCRM"
        print address
        if len(self.locs) == 0:
            base = "https://maps.googleapis.com/maps/api/geocode/json?"
            addressurl = base + address + key
            req = urllib2.Request(addressurl)
            html = urllib2.urlopen(req).read()
            addressdata = json.loads(html)
            for i in addressdata['results']:
                self.locs.append([i["formatted_address"],
                str(i['geometry']['location']['lat'])+","+str(i['geometry']['location']['lng'])])
        if len(self.locs) > 1:
            return self.locs," ".join([i for i in self.args if not i in d]+others)
        if len(self.locs) == 0:
            print "location not found, please try again"
            return None, None

        location = self.locs[0][1]
        location = "location=" + location

        base = "https://maps.googleapis.com/maps/api/place/radarsearch/json?"

        radius = "&radius=5000"

        final = base+location+radius+types+keywords+key
        print final
        req = urllib2.Request(final)
        html = urllib2.urlopen(req).read()
        data = json.loads(html)
        base2 = "https://maps.googleapis.com/maps/api/place/details/json?"
        results = {};resultsratings = {}
        for i in range(4):
            try:
                placeid = "placeid=" + data['results'][i]['place_id']
            except IndexError:
                if i==0:
                    print("no results found")
                    break
                pass

            placeurl = base2 + placeid + key
            req = urllib2.Request(placeurl)
            html = urllib2.urlopen(req).read()

            placedata = json.loads(html)
            if 'user_ratings_total' in placedata['result']:
                resultsratings[placedata['result']['name']] = int(placedata['result']['user_ratings_total'])
            else:
                resultsratings[placedata['result']['name']]=0
            results[placedata['result']['name']] = []
            if 'formatted_address' in placedata['result']:
                results[placedata['result']['name']].append(placedata['result']['formatted_address'])
            else:
                results[placedata['result']['name']].append("address not found")
            if 'formatted_phone_number' in placedata['result']:
                results[placedata['result']['name']].append(placedata['result']['formatted_phone_number'])
            elif 'international_phone_number' in placedata['result']:
                results[placedata['result']['name']].append(placedata['result']['international_phone_number'])
            else:
                results[placedata['result']['name']].append("telephone not found")

        resultsort = sorted(resultsratings.items(), key=operator.itemgetter(1), reverse=True)
        return results, resultsort

    def check_location(self, inp):
        found = True
        index = None
        if len(self.history) == 0:
            return False, None
        for j in self.history:
            for i in inp.split():
                if i in j.split():
                    continue
                else:
                    found = False
            if found:
                index = j
                break
        return found, index