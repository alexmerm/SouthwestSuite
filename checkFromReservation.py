import checkin
import checkPrice
import json

if __name__ == '__main__':
    reservation = checkin.lookup_existing_reservation('NARZLA', 'ALEXANDER', 'KAISH')
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

        date = reservation['bounds'][0]['departureDate']
        origin = reservation['bounds'][0]['departureAirport']['code']
        dest = reservation['bounds'][0]['arrivalAirport']['code']
        checkPrice.auto_checkLower(date,origin,dest,flightnum,'1','900', '1')
        print flightnum
        print flightnum == '1373/40'

