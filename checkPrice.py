
import requests
import sys
import time
import json
from twilio.rest import Client
from flightClass import Flight

with open('config.json', 'r') as fp:
    keys = json.load(fp)

#Twilio API Info
# Your Account SID from twilio.com/console
account_sid = keys['twilio_account_sid']
# Your Auth Token from twilio.com/console
auth_token  = keys['twilio_auth_token']
Phone_Num = keys['phone_num']
client = Client(account_sid, auth_token)

#southwest API Info
API_KEY = 'l7xxb3dcccc4a5674bada48fc6fcf0946bc8'
USER_EXPERIENCE_KEY = 'AAAA3198-4545-46F4-9A05-BB3E868BEFF5'
BASE_URL = 'https://mobile.southwest.com/api/'
CHECKIN_EARLY_SECONDS = 5
CHECKIN_INTERVAL_SECONDS = 0.25
MAX_ATTEMPTS = 40

# Pulled from proxying the Southwest iOS App
headers = {'Host': 'mobile.southwest.com', 'Content-Type': 'application/json', 'X-API-Key': API_KEY, 'X-User-Experience-Id': USER_EXPERIENCE_KEY, 'Accept': '*/*'}

# You might ask yourself, "Why the hell does this exist?"
# Basically, there sometimes appears a "hiccup" in Southwest where things
# aren't exactly available 24-hours before, so we try a few times
def safe_request(url, body=None):
    attempts = 0
    while True:
        if body is not None:
            r = requests.post(url, headers=headers, json=body)
        else:
            r = requests.get(url, headers=headers)
        data = r.json()
        if 'httpStatusCode' in data and data['httpStatusCode'] in ['NOT_FOUND', 'BAD_REQUEST', 'FORBIDDEN']:
            attempts += 1
            print(data['message'])
            if attempts > MAX_ATTEMPTS:
                sys.exit("Unable to get data, killing self")
            time.sleep(CHECKIN_INTERVAL_SECONDS)
            continue
        return data
    
    #Date format YYYY-MM-DD
def do_flight_search(date, origin, dest, passengers):
    """
    Find Existing Flight, returns FlightGroup
    :param date: Date in format YYYY-MM-DD
    :param origin: Origin 3 char code
    :param dest:  dest 3 char code
    :param passengers: # passengers
    :return: FlightGroup(Group of Cards of flights from API)
    """
    # Find our existing record
    url = "{}mobile-air-booking/v1/mobile-air-booking/page/flights/products?origination-airport={}&destination-airport={}&departure-date={}&number-adult-passengers={}&number-senior-passengers=0&currency=USD".format(BASE_URL, origin, dest, date, passengers)
    data = safe_request(url)
    cards = data['flightShoppingPage']['outboundPage']['cards']
    results = []
    for card in cards:
        results.append(Flight.initFromCard(card,origin,dest,date,passengers))
    #Verify??
    print results
    return results


def get_fare(flight):
    """
        get_fare(flight)
        send Flight card from Southwest API
    :param flight: Flight card from Southwest API
    :return: int of lowest price or None if no price available
    """
    if(flight['startingFromPrice']):
        return int(flight['startingFromPrice']['amount'])
    else:
        return None

def lowest_fare(flights):
    """
    lowest_fare(flightgroup)
    Get lowest Fare in FlightGroup, Possibly implement restrictions in Future
    :param flightGroup: Flight Cards Group
    :return: Array of flight units of Flights with same lowest price, None if no flights are available
    """
    lowFare = 200000000000;
    cheapestFlights = []
    for flight in flights:
        fare = flight.fare
        if fare == None:
            print('Flight {} is no longer available\n').format(flight['flightNumbers'])
        elif fare < lowFare:
            cheapestFlights = [flight]
            lowFare = fare
        elif fare == lowFare:
            cheapestFlights.append(flight)

    return cheapestFlights


def get_flight(flights, flightNo):
    """
    get_flight(flightGroup, flightNo)
    :param flightGroup: Group of Cards of Flights
    :param flightNo: String of FlightNo, if conntecting in formal 'first/last' ex: '1373/40'
    :return: Flight Unit if in group, none otherwise
    """
    print flights
    for flight in flights:
        print flight
        if flight.number == flightNo:
            return flight;
    return None

def get_flight_fare(date, origin, dest, flightNo, passengers):
    """
    Gets flight Fare for Flight # on Date for X passengers
    :param date: Date in format YYYY-MM-DD
    :param origin: Origin 3 char code
    :param dest: Dest 3 char code
    :param flightNo: String of FlightNo, if conntecting in formal 'first/last' ex: '1373/40'
    :param passengers: # passengers(in string)
    :return: int of Flight Fare, None if not found
    """
    flights = do_flight_search(date, origin, dest, passengers)
    flight = get_flight(flights, flightNo)
    if flight:
        flight.fare
    else:
        return None

def get_lowest_fare(date, origin, dest, passengers):
    flights = do_flight_search(date,origin,dest,passengers)
    flights = lowest_fare(flights)
    if flights:
        return flights
    else:
        return 0

def auto_checkLower(date, origin, dest, flightNo, passengers, lowFare, checkAlts,phoneNo):
    lowFare = int(lowFare)
    checkAlts = int(checkAlts)
    body = None
    cheaperFare = False #for if orig flight has cheaper fare
    cheaperFlight = False #for if alt flight has cheaper fare
    print('\nChecking fare for flight {} on {} from {} to {} with {} passengers\n').format(flightNo, date, origin, dest, passengers)
    flights = do_flight_search(date,origin,dest,passengers)
    origFlight = get_flight(flights, flightNo)
    if not origFlight:
        print("Flight {} on {} from {} to {} for {} passengers was not found, quitting function\n").format(flightNo,date, origin, dest, passengers)
        return
    fare = int(origFlight.fare)

    if(fare == None):
        print("Flight {} is sold out\n").format(flightNo)
    elif(fare < lowFare):
        savings = lowFare - fare
        body =  ("LOWER FARE FOUND for Flight {} from {} to {} on {}\nPrice dropped from ${} to ${}, saving ${}\nRebook Now\n").format(flightNo, origin, dest, date, lowFare, fare, savings)
        print('Found Lower fare for flight {} : ${}\nYou Saved ${}').format(flightNo, fare, savings)
        lowFare = fare
        cheaperFare = True
    elif fare > lowFare:
        print('The fare for flight {} went up from ${}! It\'s now ${}\n').format(flightNo,lowFare,fare)
    else:
         print('Fare for flight {} stayed at ${}\n').format(flightNo,fare)
    lowOrigFlightFair = lowFare
    if(checkAlts):
        cheapestFlights = lowest_fare(flights)
        if cheapestFlights:
            sameFlight = False
            for flight in cheapestFlights:
                sameFlight = sameFlight or flight['flightNumbers'] == origFlight['flightNumbers']
            if(not sameFlight):
                fare = int(cheapestFlights[0].fare)
                if(fare < lowFare):
                    savings = lowFare - fare
                    cheaperFlight = True
                    print("Found Cheapest Alternative Flight(s): They cost ${} saving ${}\n Flight(s):\n").format(fare, savings)
                    if len(cheapestFlights) > 1:
                        if(body):
                            body+= "Found Cheaper Alternative Flight: They cost ${} saving an additional ${}\nFlights:\n".format(fare,savings)
                        else:
                            body = "CHEAPER FLIGHTS FOUND for your trip from {} to {} on {}\nThey cost ${} saving ${}\nFlights:\n".format(origin, dest,date, fare, savings)
                    else:
                        if(body):
                            body+= "Found Cheaper Alternative Flight: It costs ${} saving an additional ${}\nFlight:\n".format(fare,savings)
                        else:
                            body = "CHEAPER FLIGHT FOUND for your trip from {} to {} on {}\nIt costs ${} saving ${}\nFlight:\n".format(origin, dest,date,fare,savings)
                    for flight in cheapestFlights:
                        flightInfo = "Depart: {} Arrive: {} Duration: {} Stops: {}\n".format(flight['departureTime'], flight['arrivalTime'],flight['duration'],flight['stopDescriptionOnSelect'])
                        print flightInfo
                        body +=flightInfo
    if(cheaperFare or cheaperFlight):
        send_Message(phoneNo,body)
    return lowOrigFlightFair

def send_Message(number,body):
    message = client.messages.create(
        to=number,
        from_=keys['from_phone_num'],
        body=body)
    #print(message.sid)


    
if __name__ == '__main__':
    if(len(sys.argv) > 1):
        if len(sys.argv) == 8:
            #Check Lower
            date = sys.argv[1]
            origin = sys.argv[2]
            dest = sys.argv[3]
            number = sys.argv[4]
            passengers = sys.argv[5]
            cost = sys.argv[6]
            checkAlt = sys.argv[7]
            #VERYIFY
            auto_checkLower(date,origin,dest,number,passengers,cost,checkAlt)


    #Tests
    #print(get_flight_fare('2019-01-04','LGA','AUS','154/9','1'))
    #num = get_lowest_fare('2019-01-03','LGA','AUS','1')
    #print('Lowest fare is {} on flight {}').format(get_flight_fare('2019-01-04','LGA','AUS',num,'1'),num)
    #auto_checkLower('2018-12-17','AUS','LGA','1250/1988','1',400, 1)
    #auto_checkLower('2019-01-04','LGA','AUS','154/9','1',400, 1)
    #auto_checkLower('2018-12-17','AUS','EWR','4695/2366','1',400, 1)
    #auto_checkLower('2018-12-17','AUS','LGA','1373/40','1',900, 0)
    #send_Message('test\n-Alex Southwest thing')
    
    
    
    
