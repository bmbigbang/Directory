import json,urllib2,operator,re
from corrector import Corrector
from options import Options,Chunks
from misc import finder,alphabet

while True:
    base = "https://maps.googleapis.com/maps/api/geocode/json?"
    print """directory section active."""
    command = raw_input("SMS in: ")
    esc = finder(r'exit',command.lower())
    if esc.found():
        break
    typfin = finder(r'type',command.lower())
    sub = False
    if typfin.found():
        
        sub = True
        while True:
            print 'send in type of place or list to see all possible types'
            comtyp = raw_input("SMS in: ")
            test = Corrector('dirtypes');types=[]
            if 'list' in comtyp.split():
                displayt = Chunks(",".join(test.commands[test.scope]),
                            footing="Type anything to continue or exit to cancel")
                displayt.create_Chunks()
                for i in displayt.chunk_list:
                    print i
                    if displayt.chunk_list.index(i)==len(displayt.chunk_list)-1:
                        break
                    print 
                    nekst = raw_input("SMS in: ")
                    esc3 = finder(r'exit',nekst.lower())
                    if esc3.found():
                        if displayt.chunk_list.index(i)==len(displayt.chunk_list)-1:
                            pass
                        else:
                            break
            esc2 = finder(r'exit',comtyp.lower())
            if esc2.found():
                break
            
            for i in test.disting(comtyp)['words']:
                try:
                    if test.match(i)[0][1] <= 2.33:
                        types.append(test.match(i)[0][0])
                except:
                    break

            if len(types)>=1:
                types = "&types=" + "|".join(types)
                break

    try:
        if len(types)==0:
            types=""
    except:
        types=""
    
                
    keyfind = finder(r'keyword',command.lower())
    if keyfind.found():
        
        sub = True
        print "enter a set of keywords or type in exit to continue."
        comkey = raw_input("SMS in: ")
        keyws = comkey.split()
    try:
        if len(keyws)>=1:
            keywords = "&keyword="+ "+".join(keyws)
    except:
        keywords = ""
        
                
    if sub == True:
        continue
        
    address = "address="
    for i in command.split():
        address+= i+"+"
    address = address[:-1]
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
        print "location not found"


    base = "https://maps.googleapis.com/maps/api/place/radarsearch/json?"

    radius = "&radius=5000"

    final = base+location+radius+types+keywords+key
    req = urllib2.Request(final)
    html = urllib2.urlopen(req).read()
    data = json.loads(html)
    print final
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
    display = Options('english',"available places found nearby:","Please choose an option. ") 
    for i in resultsort:
        display.add_Option(content="{0} - Ratings : {1}".format(i[0].encode('utf-8'),str(i[1])))
    displayc = Chunks(display.print_Options(),footing="Type anything to continue or exit to cancel")
    displayc.create_Chunks()
    for i in displayc.chunk_list:
        print i
        if displayc.chunk_list.index(i)==len(displayc.chunk_list)-1:
            break
        nekst = raw_input("SMS in: ")
        if "exit" in nekst:
            break

    while True:
        choice = raw_input("SMS in: ").lower()
        choices = alphabet(test.lang[test.langsel])
        try:
            choice = display.select_Option(choice)
            break
        except:
            print "choice not recognised, please try again" 
            choice = raw_input("SMS in: ").lower()

    text = "{0} - Ratings : {1}".format(resultsort[choice][0],resultsort[choice][1])   
    text += "\n Address: "+results[resultsort[choice][0]][0]
    text += "\n" +" Telephone Number: " + results[resultsort[choice][0]][1]
                                
    displayc = Chunks(text,footing="Type anything to continue or exit to cancel")
    displayc.create_Chunks()
    for i in displayc.chunk_list:
        print i
        if displayc.chunk_list.index(i)==len(displayc.chunk_list)-1:
            break
        nekst = raw_input("SMS in: ")
        if "exit" in nekst:
            break
            
    

