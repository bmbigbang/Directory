

class Helper(str):
    
    def __init__(self):
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
add a <text> to either of the above commands to include a message in your reminder""",
                        'main':"""use directory or time to access these modules"""}

        self.list = []
        for i in self.helper:
            self.list.append(i)
    
    def entitymap(self):
        ent = {'PERSON':'People, including fictional.',
             'NORP':'Nationalities or religious or political groups.',
             'FACILITY':'Buildings, airports, highways, bridges, etc.',
             'ORG':'Companies, agencies, institutions, etc.',
             'GPE':'Countries, cities, states.',
             'LOC':'Non-GPE locations, mountain ranges, bodies of water.',
             'PRODUCT':'Vehicles, weapons, foods, etc. (Not services)',
            'EVENT':'Named hurricanes, battles, wars, sports events, etc.',
            'WORK_OF_ART':'	Titles of books, songs, etc.',
            'LAW':'Named documents made into laws',
            'LANGUAGE':'Any named language',
            'DATE':'Absolute or relative dates or periods',
            'TIME':'Times smaller than a day',
            'PERCENT':'Percentage (including %)',
            'MONEY':'Monetary values, including unit',
            'QUANTITY':'Measurements, as of weight or distance',
            'ORDINAL':'first", "second"',
            'CARDINAL':'Numerals that do not fall under another type'}
        return ent
    def dirtypes(self):
        dirs = ['accounting','airport','amusement_park',
                         'aquarium','art_gallery','atm','bakery',
'bank','bar','beauty_salon','bicycle_store','book_store','bowling_alley',
'bus_station','cafe','campground','car_dealer','car_rental','car_repair',
'car_wash','casino','cemetery','church','city_hall','clothing_store',
'convenience_store','courthouse','dentist','department_store','doctor',
'electrician','electronics_store','embassy','establishment','finance',
'fire_station','florist','food','funeral_home','furniture_store',
'gas_station','general_contractor','grocery_or_supermarket','gym',
'hair_care','hardware_store','health','hindu_temple','home_goods_store',
'hospital','insurance_agency','jewelry_store','laundry','lawyer','library',
'liquor_store','local_government_office','locksmith','lodging','meal_delivery',
'meal_takeaway','mosque','movie_rental','movie_theater','moving_company',
'museum','night_club','painter','park','parking','pet_store','pharmacy',
'physiotherapist','place_of_worship','plumber','police','post_office',
'real_estate_agency','restaurant','roofing_contractor','rv_park','school',
'shoe_store','shopping_mall','spa','stadium','storage','store',
'subway_station','synagogue','taxi_stand','train_station','travel_agency',
'university','veterinary_care','zoo']
        return dirs
    
    def foodtypes(self):
        foods = ["italian","pizza","bacon","mexican","chinese","japanese",
                 "barbeque","vietnamese","food","takeaway","delivery",
                 "restaraunt","cafe","vegetarian","lebanese","indian","menu",
                 "thai","indonesian","grill","bar","french","seafood","vegan"]
        return foods
    
    def addresstypes(self):
        places = ["london","uk","manchester","new_york","city","postcode",
                  "address", "street","county","state","postal"]
        return places

    def __str__(self,scope="main",detail=""):
        return self.helper[scope+detail]

##test = Helper('dine')
##print test
##test.scope = 'time'
##print test
##test.detail = 'schedule'
##print test
