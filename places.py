import json,urllib2,operator,re,urllib
from options import Options,Chunks
from misc import finder,alphabet
from helper import Helper

class Directory(object):
    hlp = Helper()
    def __init__(self,args):
        self.args = args
        
    def run(self,types,keywords,others):
        types = "&types=" + "|".join(types)
        keywords= "&keyword="+ "+".join(keywords)
        address = "address="+"+".join(self.args+others)
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
                break

        
            base = "https://maps.googleapis.com/maps/api/place/radarsearch/json?"
        
            radius = "&radius=5000"
        
            final = base+location+radius+types+keywords+key
            req = urllib2.Request(final)
            html = urllib2.urlopen(req).read()
            data = json.loads(html)
            print final
        
            base2 = "https://maps.googleapis.com/maps/api/place/details/json?"
            results = {};resultsratings = {}
            for i in range(4):
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
            return results,resultsort
#            opts = Options() 
#            for i in resultsort:
#                opts.add_Option(content="{0} - Ratings : {1}".format(i[0].encode('utf-8'),str(i[1])))
#            display = Chunks(opts.print_Options())
#            display.create_Chunks(heading="Available places found nearby:",
#                              footing="Type next-back-find or choose an option. ")
#            print display.goto_Chunk()
#            option = raw_input("SMS in: ")
#            if opts.select_Option(option)!=None:
#                text = "{0} - Ratings : {1}".format(resultsort[ch][0],resultsort[ch][1])
#                text += "\n" +" Telephone Number: " + results[resultsort[ch][0]][1]
#                text += "\n Address: "+results[resultsort[ch][0]][0]
#                displayc = Chunks(text)
#                displayc.create_Chunks()
#                print display.goto_Chunk()


            
    

