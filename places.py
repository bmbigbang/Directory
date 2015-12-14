import json,urllib2,operator,re
from options import Options,Chunks
from misc import finder,alphabet
from helper import Helper
global hlp
hlp = Helper()

class Directory(object):
    def __init__(self,args):
        self.args = args
        
    def run(self,resu,resu2,types,keywords,others):
        types2="";keywords2="";address2=""
        while True:
            base = "https://maps.googleapis.com/maps/api/geocode/json?"
            print """directory section active."""
            if 'list' in self.args:
                print "List of types of places:"
                displayt = Chunks(",".join(hlp.dirtypes()))
                displayt.create_Chunks(footing="Type next-back-find or exit to cancel")
                displayt.display_Chunks()
                continue
            if 'exit' in self.args:
                break

            if len(types)>1 and len(types2)==0:
                types2 = "&types=" + "|".join([h[0] for h in types])
            elif len(types)==1 and len(types2)==0:
                types2 = "&types={0}".format(types[0][0])
            elif len(types2)>0:
                pass
            else:
                types2 = ""
      
            if len(keywords)>=2 and len(keywords2)==0:
                keywords2 = "&keyword="+ "+".join(keywords)
            elif len(keywords)==1 and len(keywords2)==0:
                keywords2 = "&keyword={0}".format(keywords[0])
            elif len(keywords2)>0:
                pass
            else:
                keywords2 = ""
                
                        
            if len(self.args+others)>=2 and len(address2)==0:
                address2 = "address="+"+".join(self.args+others)
            elif len(self.args+others)==1 and len(address2)==0:
                address2 = "address={0}".format((self.args+others)[0])
            elif len(address2)>0:
                pass
            else:
                address2 = ""

            key="&key=AIzaSyAgcnAoMCuhgMwXLXwRuGiEZmP0T-oWCRM"
            addressurl = base + address2 + key
            
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
                break

        
            base = "https://maps.googleapis.com/maps/api/place/radarsearch/json?"
        
            radius = "&radius=5000"
        
            final = base+location+radius+types2+keywords2+key
            req = urllib2.Request(final)
            html = urllib2.urlopen(req).read()
            data = json.loads(html)
            print final
            
            ##radius changing code:
            ##for i in range(2):
            ##    with urllib.request.urlopen(final) as response:
            ##        html = response.read().decode()
            ##    data = json.loads(html)
            ##    if len(data['results']) > 3:
            ##        radius = "&radius=" + str(int(int(radius[(radius.find("=")+1):])/ 1.2))
            ##        final = base+location+radius+types+keyword+key
        
            base2 = "https://maps.googleapis.com/maps/api/place/details/json?"
            results = {};resultsratings = {}
            for i in range(3):
                try:
                    placeid = "placeid=" + data['results'][i]['place_id']
                except IndexError:
                    if i==0:
                        print("no results found")
                        break
                    break
                        
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
            display = Options('english',heading="Available places found nearby:",
                              footing="Type next-back-find or choose an option. ") 
            for i in resultsort:
                display.add_Option(content="{0} - Ratings : {1}".format(i[0].encode('utf-8'),str(i[1])))
            ch = display.select_Option(display.print_Options())
            if ch == 'exit':
                break
            if ch!=None:
                text = "{0} - Ratings : {1}".format(resultsort[ch][0],resultsort[ch][1])   
                text += "\n Address: "+results[resultsort[ch][0]][0]
                text += "\n" +" Telephone Number: " + results[resultsort[ch][0]][1]
                displayc = Chunks(text)
                displayc.create_Chunks(footing="Type next-back-find or exit to cancel")
                displayc.display_Chunks()    
                break

            
    

