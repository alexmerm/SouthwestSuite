class Flight(object):

    def __init__(self,number, origin, dest,date, passengers, fare):
        self.date = date
        self.number = number
        self.origin = origin
        self.dest = dest
        self.passengers = passengers
        self.fare = fare
        self.hasTimeInfo = False
    @classmethod
    def initFromCard(cls, flightCard, origin, dest, date, pasengers):
        """
        Init from Flight object From Search
        :param flightCard:
        :param origin:
        :param dest:
        :param date:
        :param pasengers:
        """
        flightObj = cls(flightCard['flightNumbers'],origin,dest,date,pasengers,flightCard['startingFromPrice']['amount'])
        flightObj.hasTimeInfo = True
        flightObj.departureTime = flightCard['departureTime']
        flightObj.arrivalTime = flightCard['arrivalTime']
        flightObj.duration = flightCard['duration']
        flightObj.stopsDesc = flightCard['stopDescription']
        return flightObj
    @classmethod
    def initFromBoundItem(cls, flightBoundItem, cost):
        num = ""
        for flightNum in flightBoundItem['flights']:
            num += "{}/".format(flightNum['number'])
        num = num[:-1]
        #print flightBoundItem
        flightObj = cls(num,flightBoundItem['departureAirport']['code'],flightBoundItem['arrivalAirport']['code'],flightBoundItem['departureDate'],'1',cost)

        flightObj.hasTimeInfo = True
        flightObj.departureTime = flightBoundItem['departureTime']
        flightObj.arrivalTime = flightBoundItem['arrivalTime']
        flightObj.duration = flightBoundItem['travelTime']
        return flightObj
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def updateFare(self,cost):
        self.fare = cost


    #DEF Validate(against orig route serch, against online?)

#DEF GetMoreInfo(self)
        #Does Flight Search, gets Time Info, Curr Price?
        #Self.available


# Put in a compare clause, check if fare is lower thn other by just comparing self