from itinerary import Itinerary
import client as cli

if __name__ == "__main__":
    departure = input("Type your departure : ")
    destination = input("Type your destination : ")

    itinerary = Itinerary(departure, destination)
    print(itinerary.get_itineraries())
