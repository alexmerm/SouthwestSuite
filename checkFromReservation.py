import checkin
import checkPrice
import json

if __name__ == '__main__':
    reservation = checkin.lookup_existing_reservation('UI88B2', 'ALEXANDER', 'KAISH')
    #print json.dumps(reservation, sort_keys=True,indent=4,separators=(',\n',':'))
    #Depart leg, Return Leg
    legs = reservation['bounds']
    for x in range(0,len(legs)):
        flights = legs[x]['flights']
        flightnum = ''
        if len(flights) == 1:
            flightnum = flights[0]['number']
        else:
            for flight in flights:
                flightnum += "{}/".format(flight['number'])
            flightnum = flightnum[:-1]

        date = reservation['bounds'][x]['departureDate']
        origin = reservation['bounds'][x]['departureAirport']['code']
        dest = reservation['bounds'][x]['arrivalAirport']['code']
        checkPrice.auto_checkLower(date,origin,dest,flightnum,'1','126', '1')
        print flightnum

