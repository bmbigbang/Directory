import json,urllib2,operator,re,urllib
from options import Options,Chunks
from misc import finder,alphabet
from helper import Helper
from spacyapi import similarity

class Directory(object):
    def __init__(self,args):
        self.args = args
        
    def run(self,disting):
        types=[];keywords=[];d=[];hlp = Helper()
        test2 = similarity(" ".join(self.args)," ".join(hlp.dirtypes()),sort=True,average=False)
        for s in self.args:
            for k in test2[s][:4]:
                if k[1]>=0.5:
                    types.append(k[0])
                    if (s in d) == False:
                        d.append(s)
        for i in d:
            keywords.append(s)
            del self.args[self.args.index(i)]
        d=[]
        test4 = similarity(" ".join(self.args)," ".join(hlp.addresstypes()),average=True) 
        for wo in test4:
            for keyword in test4[wo]:
                if keyword[-1]>=0.5:
                    break
                elif (i in d) == False:
                    d.append(i)
        for i in d:
            del self.args[self.args.index(i)] 
        others=disting['numbers']+disting['splits']
        
        types = "&types=" + "|".join(types)
        keywords= "&keyword="+ "+".join(keywords)
        address = "address="+"+".join(self.args+others)
        base = "https://maps.googleapis.com/maps/api/geocode/json?"
        print """directory section active."""

        key="&key=AIzaSyAgcnAoMCuhgMwXLXwRuGiEZmP0T-oWCRM"
        addressurl = base + address + key
        req = urllib2.Request(addressurl)
        html = urllib2.urlopen(req).read()
        addressdata = json.loads(html)
        try:
            lat = str(addressdata['results'][0]['geometry']['location']['lat'])
            lng = str(addressdata['results'][0]['geometry']['location']['lng'])
            location= lat+","+ lng
            location = "location=" + location
        except IndexError:
            print "location not found, please try again"
            return None, None

        base = "https://maps.googleapis.com/maps/api/place/radarsearch/json?"
    
        radius = "&radius=5000"
    
        final = base+location+radius+types+keywords+key
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
                resultsratings[placedata['result']['name']]=int(placedata['result']['user_ratings_total'])
            else:
                resultsratings[placedata['result']['name']]=0
            results[placedata['result']['name']]=[]
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
        
        resultsort = sorted(resultsratings.items(),key = operator.itemgetter(1),reverse=True)
        return results,resultsort


            
    

