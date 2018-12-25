class Flight:
    def __int__(self,number, origin, dest,date, passengers, fare):
        self.date = date
        self.number = number
        self.origin = origin,
        self.dest = dest
        self.passengers = passengers
        self.fare = fare
        self.hasTimeInfo = False
    @classmethod
    def initFromCard(self, flightCard, origin, dest, date, pasengers):
        """
        Init from Flight object From Search
        :param flightCard:
        :param origin:
        :param dest:
        :param date:
        :param pasengers:
        """
        self.__init__(flightCard['flightNumbers'],origin,dest,date,pasengers,flightCard['startingFromPrice']['amount'])
        self.hasTimeInfo = True
        self.departureTime = flightCard['departureTime']
        self.arrivalTime = flightCard['arrivalTime']
        self.duration = flightCard['duration']
        self.stopsDesc = flightCard['stopDescription']
    @classmethod
    def initFromBoundItem(self, flightBoundItem, cost):
        self.number = flightBoundItem
        self.date = flightBoundItem['departureDate']
        self.origin = flightBoundItem['departureAirport']['code']
        self.dest = flightBoundItem['arrivalAirport']['code']
        self.fare = cost
        self.hasTimeInfo = True
        self.departureTime = flightBoundItem['departureTime']
        self.arrivalTime = flightBoundItem['arrivalTime']
        self.duration = flightBoundItem['travelTime']
        num = ""
        for flight in flightBoundItem['flights']:
            num += "{}/".format(flight['number'])
        self.number = num[:-1]


    #DEF Validate(against orig route serch, against online?)
class FlightReservation(Flight):
    pass

if(__name__ == '__main__'):
    pass



# Put in a compare clause, check if fare is lower thn other by just comparing self