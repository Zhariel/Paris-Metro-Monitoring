from itinerary import Itinerary
from client import NavitiaClient

if __name__ == "__main__":
    departure = "108 rue Perthuis, 92140 Clamart"
    destination = "242 Rue du Faubourg Saint-Antoine, 75012 Paris"

    itinerary = Itinerary(departure, destination)
    print(itinerary.get_itineraries())

    client = NavitiaClient()
    client.get_all_Metro_lines_json()
    client.get_all_Bus_lines_json()
    client.get_all_Tramway_lines_json()
    client.get_all_LocalTrains_lines_json()
    client.get_all_RapidTransit_lines_json()