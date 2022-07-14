from itinerary import Itinerary
import client as cli

if __name__ == "__main__":
    
    departure = "La Courneuve - May 8, 1945"
    destination = "Aubervilliers-Pantin Quatre Chemins"
    
    itinerary = Itinerary(departure, destination)
    print(itinerary.get_itineraries().iloc[0]["sections"])
