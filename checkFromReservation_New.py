import checkin
import checkPrice
import json
from flightClass import Flight

if __name__ == '__main__':
    reservation = checkin.lookup_existing_reservation('UI88B2', 'ALEXANDER', 'KAISH')
    #print json.dumps(reservation, sort_keys=True,indent=4,separators=(',\n',':'))
    #Depart leg, Return Leg
    legs = reservation['bounds']
    for f in legs:
        ##each legs[x] is one leg of the flight, or one flight

        fl = Flight.initFromBoundItem(f,500)
        checkPrice.auto_checkLower(fl.date,fl.origin,fl.dest,fl.flightnum,fl.passengers,fl.fare)
        #checkPrice.auto_checkLower(date,origin,dest,flightnum,'1','900', '1')

