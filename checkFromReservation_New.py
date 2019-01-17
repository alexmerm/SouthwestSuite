import checkin
import checkPrice
import json
from flightClass import Flight

if __name__ == '__main__':
    reservation = checkin.lookup_existing_reservation('SOXX2F', 'Steven', 'Kaish')
    #print json.dumps(reservation, sort_keys=True,indent=4,separators=(',\n',':'))
    #Depart leg, Return Leg
    legs = reservation['bounds']
    for f in legs:
        ##each legs[x] is one leg of the flight, or one flight

        fl = Flight.initFromBoundItem(f,100)
        checkPrice.auto_checkLower(fl.date,fl.origin,fl.dest,fl.number,fl.passengers,fl.fare,1)
        #checkPrice.auto_checkLower(date,origin,dest,flightnum,'1','900', '1')

