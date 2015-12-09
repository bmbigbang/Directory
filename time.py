import time,pytz,re
from datetime import datetime,timedelta
from misc import finder
from corrector273 import Corrector


timezonelist = { 'london':'Europe/London', 'paris':'Europe/Paris',
                 'sydney':'Australia/Sydney', 'san fransisco':'America/Los_Angeles' }
grammar = ['in' ,'at', 'between', 'help', 'schedule']
location = 'london'
fmt = "%d-%m-%Y %H:%M:%S %Z%z"

def time(words,times,current='time'):
    locs = Corrector('locations');locations = []
    while True:
        found = False;terminate = False
        for k in words:
            if locs.match(k) >= 2.33:
                locations+=k
        if len(words) ==2 and 'now' in words:
            print datetime.now(pytz.timezone(timezonelist[location])).strftime(fmt)
            continue
        for i in words:
            finddiff = finder(r'^diff',i)
            findbet = finder(r'^betw',i)
            if 'between' in words or finddiff.found():
                showtimedate = datetime.now(pytz.timezone(timezonelist[i])).strftime('%Y%m%d')
            try:
                loctime1 = datetime.now(pytz.timezone(timezonelist[i])).strftime('%H')
                loctime2 = datetime.now(pytz.timezone(timezonelist[location])).strftime('%H')
                final = int(loctime1)-int(loctime2)
            except:
                print("error with cities entered")
                continue
        finderdate = finder(r'\b[0-9]{8}\b',command)
        if finderdate.found():
            finderdatestring = finderdate.result()
            try:
                showtime = datetime(int(finderdatestring[4:]),int(finderdatestring[2:4]),
                            int(finderdatestring[:2]),int(finderstring[:2])-final,
                            int(finderstring[2:]),0,0,pytz.timezone(timezonelist[location]))
                finderdatestring = finderdatestring[:2] + "/" + finderdatestring[2:4] + "/" + finderdatestring[4:]
            except ValueError:
                print("incorrect date entered")
                found = True
                continue
        else:
            showtime = datetime(int(showtimedate[:4]),int(showtimedate[4:6]),
                            int(showtimedate[6:]),int(finderstring[:2])-final,
                            int(finderstring[2:]),0,0,pytz.timezone(timezonelist[location]))
            finderdatestring = ""
     
            finalshowtime = finderstring + " "  + finderdatestring
            print("{0} in {1} is {2} in {3}".format(finalshowtime,i,showtime.strftime(fmt),location))

        
        if 'help' in words:
            if 'schedule' in words:
                print("""entering [city name] will change current location and scheduling is \n
    based on current location. send [schedule in <4 digit time 1650> ] to schedule \n
    reminder in 16 hours and 50 mins. send [schedule at <hhmm eg. 1650> \n
    <ddmmyyyy eg. 25052016]>] to schedule reminder at 16:50 on 25/5/2016 \n
    add a <text> to either of the above commands to include a message in your reminder""")
                found = True
                continue
            else:
                print("""Usage: send [<city name>] to set current location and see the time or \n
    [between <city> <city>] to see the time difference between two cities. Use [<city name> <4 digit \n
    time hhmm>] to show a specific time in a different city converted to local time \n
    more help with reminders available with [help schedule]""")
                found = True
                continue



        if 'schedule' in words:
            if 'at' in words:
                year = int(datetime.now(pytz.timezone('Europe/London')).strftime('%Y'))
                findertime1 = finder(r'\b[0-9]{4}\b',command)
                if findertime1.found()==False:
                    print("The entered time to schedule reminder for should be 4 digits <hhmm>")
                    continue
                try:
                    assert int(findertime1.result()[2:]) <= 59 and int(findertime1.result()[2:]) >= 0
                except:
                    print("The entered minutes must be between 00 and 59")
                    continue
                try:
                    assert int(findertime1.result()[:2]) <= 23 and int(findertime1.result()[:2]) >=0
                except:
                    print("The entered hours must be between 00 and 23")
                    continue
                finderdate1 = finder(r'\b[0-9]{8}\b',command)
                if finderdate1.found():
                    try:
                        assert int(finderdate1.result()[:2]) <= 31 and int(finderdate1.result()[:2]) >=1
                    except:
                        print("The entered day must be between 01 and 31")
                        continue
                    try:
                        assert int(finderdate1.result()[2:4]) <=12 and int(finderdate1.result()[2:4]) >=1
                    except:
                        print("The entered month must be between 01 and 12")
                        continue
                    try:
                        assert int(finderdate1.result()[4:]) <= year+5 and int(finderdate1.result()[4:]) >= year
                    except:
                        print("The entered year can only be 5 years in the future")
                        continue
                    reminder = datetime(int(finderdate1.result()[4:]),int(finderdate1.result()[2:4]),
                                int(finderdate1.result()[:2]),int(findertime1.result()[:2]),
                                int(findertime1.result()[2:]),0,0,pytz.timezone(timezonelist[location]))
                else:
                    finderdate11 = datetime.now(pytz.timezone(timezonelist[location])).strftime('%d%m%Y')
                    reminder = datetime(int(finderdate11[4:]),int(finderdate11[2:4]),
                                    int(finderdate11[:2]),int(findertime1.result()[:2]),
                                    int(findertime1.result()[2:]),0,0,pytz.timezone(timezonelist[location]))
                for i in words:
                    if i!='schedule' and re.search(r'[0-9]{4}',i)==None:
                        if (i in grammar) == False:
                            if re.search(r'[0-9]{8}',i)==None:
                                print("reminder ( {0} ) set for {1}".format(i,reminder.strftime(fmt)))
                                terminate=True
                                continue
                if terminate==False:
                    print("reminder set for {0}".format(reminder.strftime(fmt)))
                found = True
                continue
            elif 'in' in words:
                findertime2 = finder(r'\b[0-9]{4}\b',command)
                now = datetime.now(pytz.timezone(timezonelist[location]))
                if findertime2.found()==False:
                    print("The reminder time <hhmm> must be four digits")
                    continue
                try:
                    assert int(findertime2.result()[2:]) <=59
                except:
                    print("The reminder minutes must be smaller than 60")
                    continue
                try:
                    assert int(findertime2.result()[:2]) <= 23 and int(findertime2.result()[:2]) >=0
                except:
                    print("The entered hours must be between 00 and 23")
                    continue
                    
                reminder1 = timedelta(hours=int(findertime2.result()[:2]),
                                      minutes=int(findertime2.result()[2:])) + now

                for i in words:
                    if re.search(r'[0-9]{4}',i)==None:
                        if (i in grammar) == False:
                            if re.search(r'[0-9]{8}',i)==None:
                                print("reminder ( {0} ) set for {1}".format(i,reminder1.strftime(fmt)))
                                terminate=True
                                continue
                if terminate==False:
                    print("reminder set for {0}".format(reminder1.strftime(fmt)))

                found = True
                continue

        
        if 'between' in words:
            locs=[]
            for i in words:
                if i in locations:
                    locs.append(i)
                
            try:
                loctime1 = datetime.now(pytz.timezone(timezonelist[locs[0]])).strftime('%H')
                loctime2 = datetime.now(pytz.timezone(timezonelist[locs[1]])).strftime('%H')
                final = int(loctime1)-int(loctime2)
            except:
                print("error with entered cities")
                continue
            if final<0:
                print("{0} is {1} hours {2} {3}".format(locs[0],str(abs(final)),"behind",locs[1]))
            else:
                print( "{0} is {1} hours {2} {3}".format(locs[0],str(abs(final)),"ahead of",locs[1]))
            found = True
            continue
        
        if found == False:
            print("command not recognized; check spelling/syntax or send [help] for support")       
    
            

