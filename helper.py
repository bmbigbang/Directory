

class Helper(str):
    
    def __init__(self,scope,detail=""):
        self.helper = {'dine':"""Enter address or location. 
Optional - You may also include a keyword (eg vegetarian): """,
                       'time':"""Usage: send [<city name>] to set current location and see the time or \n
[between <city> <city>] to see the time difference between two cities. Use [<city name> <4 digit \n
time hhmm>] to show a specific time in a different city converted to local time \n
more help with reminders available with [help schedule]""",
                       'timeschedule':"""entering [city name] will change current location and scheduling is \n
based on current location. send [schedule in <4 digit time 1650> ] to schedule \n
reminder in 16 hours and 50 mins. send [schedule at <hhmm eg. 1650> \n
<ddmmyyyy eg. 25052016]>] to schedule reminder at 16:50 on 25/5/2016 \n
add a <text> to either of the above commands to include a message in your reminder"""}
        self.scope = scope
        self.detail = detail

    def __str__(self):
        return self.helper[self.scope+self.detail]

##test = Helper('dine')
##print test
##test.scope = 'time'
##print test
##test.detail = 'schedule'
##print test
