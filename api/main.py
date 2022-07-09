import itinerary as iti
import client as cli

if __name__ == "__main__":
    departure = input("Type your departure : ")
    destination = input("Type your destination : ")

    itin = iti.Itinerary(departure, destination)
    print(itin.get_itineraries())
