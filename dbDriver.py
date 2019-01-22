import sqlite3
import os.path
import datetime
import checkPrice
import checkin
from flightClass import Flight
import json

with open('config.json', 'r') as fp:
    keys = json.load(fp)

creatingDB = not os.path.isfile('./southwest.db')
conn = sqlite3.connect('southwest.db');
c = conn.cursor()

if creatingDB:
    c.execute('''CREATE TABLE Flights(
confirmation  TEXT,
firstName TEXT,
lastName TEXT,
flightNo TEXT NOT NULL,
origin TEXT NOT NULL,
destination TEXT NOT NULL,
date TEXT  NOT NULL,
fare INT  NOT NULL,
altFlights INT NOT NULL,
phoneNo TEXT NOT NULL
);''')

def checkall():
    flights = getFlights()
    for flight in flights:
        confirmation = flight[0]
        first = flight[1]
        last = flight[2]
        flightNo = flight[3]
        origin = flight[4]
        dest = flight[5]
        dateString = flight[6]
        fare = flight[7]
        altFlights = flight[8]
        phoneNo = flight[9]

        #check if flight already happened
        date = datetime.datetime.strptime(dateString,'%Y-%m-%d')
        if (date - datetime.datetime.today()) < datetime.timedelta():
            #if in past
            #remove from DB
            pass
        else:
            #if not in past keep going
            #Veify Confirmation??
            newFare = checkPrice.auto_checkLower(dateString, origin, dest, flightNo, 1, fare, altFlights, phoneNo )
            if newFare < fare:
                c.execute("""UPDATE Flights set fare=? where flightNo=? AND phoneNo=?""",(newFare,flightNo,phoneNo,))
                conn.commit()


def getFlights():
    c.execute('SELECT * FROM Flights ORDER BY confirmation ASC')
    return c.fetchall()

def add_Flight_FromClass(confirmation,first,last,phoneNo,fl):
    add_Flight_wconfim(confirmation,first,last,fl.number,fl.origin,fl.dest,fl.date,fl.fare,0,phoneNo)

def add_Flight_wconfim(confirmation, first, last, flightno, origin, dest, date, fare, altflights,phoneNo):
    flightno = str(flightno)
    c.execute('SELECT * FROM Flights WHERE flightNo=? and phoneNo = ?', (flightno,phoneNo));
    if c.fetchone():
        print "already inserted"
        #VERIFY INFO

    else:
        c.execute("""INSERT INTO Flights (confirmation,firstName, lastName, flightNo,origin,destination,date,fare,altFlights,phoneNo) VALUES (?,?,?,?,?,?,?,?,?,?) """,(confirmation,first,last,str(flightno),origin,dest,date,str(fare),str(altflights),phoneNo,))
        conn.commit()

def add_Flight_woconfim(flightno, origin, dest, date, fare, altflights,phoneNo):
    flightno = str(flightno)
    c.execute('SELECT * FROM Flights WHERE flightNo=? and phoneNo = ?', (flightno,phoneNo));
    if c.fetchone():
        print "already inserted"
        #VERIFY INFO

    else:
        c.execute("""INSERT INTO Flights (flightNo,origin,destination,date,fare,altFlights,phoneNo) VALUES (?,?,?,?,?,?,?) """,(str(flightno),origin,dest,date,str(fare),str(altflights),phoneNo,))
        conn.commit()


def add_from_confirmation_prompt():

    while True:
        confirmation = raw_input("Enter Confirmation # : ")
        while len(confirmation) != 6:
            print "Confirmation # must be 6 characters"
            confirmation = raw_input("Enter Confirmation # : ")

        first = raw_input("Enter First Name : ");
        last = raw_input("Enter Last Name : ")
        reservation = checkin.lookup_existing_reservation(confirmation,first,last)
        if('bounds' in reservation):
            #if Reservtion Found Sucessefully
            break
        else:
            print "Reservation was not found : {}".format(reservation)


    # print json.dumps(reservation, sort_keys=True,indent=4,separators=(',\n',':'))
    # Depart leg, Return Leg
    legs = reservation['bounds']
    for f in legs:
        ##each legs[x] is one leg of the flight, or one flight

        fl = Flight.initFromBoundItem(f, 100000)
        fare = raw_input("How much did you pay flight #{} from {} to {} on {}? ".format(fl.number,fl.origin,fl.dest,fl.date))
        fl.updateFare(fare)
        add_Flight_FromClass(confirmation,first,last,keys['phone_num'],fl)
        #add_Flight_wconfim(confirmation, first, last, fl.number, fl.origin, fl.dest, fl.date, fl.fare, 0, keys['phone_num'])
        #checkPrice.auto_checkLower(fl.date, fl.origin, fl.dest, fl.number, fl.passengers, fl.fare, 1, keys['phone_num'])
        # checkPrice.auto_checkLower(date,origin,dest,flightnum,'1','900', '1')


if __name__ == '__main__':
    #add_Flight_wconfim('SOXX2F','STEVEN','KAISH',2296,'LGA','DEN','2019-02-25',120,'1',keys['phone_num'])
    #add_Flight_woconfim(2297,'LGA','DEN','2019-02-25',100,'1','+')
    #add_from_confirmation_prompt()
    checkall()
    conn.close()
