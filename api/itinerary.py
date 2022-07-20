from settings import HEADERS, URL_BASE, LINES_ENDPOINT, JOURNEYS_ENDPOINT
from split_data import get_places, format_itineraries
import requests


class Itinerary:
    def __init__(self, departure, destination):
        self.headers = HEADERS
        self.url_base = URL_BASE
        self.departure = departure
        self.destination = destination

    def __send_request(self, arg):
        uurl = self.url_base + arg
        response = requests.get(uurl, headers=self.headers).json()

        return response

    def get_address(self, addr):
        arg = "places?q=" + addr
        response = self.__send_request(arg)
        places = response["places"]
        possible_addresses = get_places(places)
        return possible_addresses

    def get_itineraries(self):
        departure = self.departure
        destination = self.destination
        id_departure = self.get_address(departure).iloc[0]["coord"]
        # print(id_departure)
        id_destination = self.get_address(destination).iloc[0]["coord"]
        # print(id_destination)

        # arg = "journeys?from=" + id_departure + "&to=" + id_destination
        arg = JOURNEYS_ENDPOINT + "?from=" + id_departure + "&to=" + id_destination
        response = self.__send_request(arg)
        journeys = response["journeys"]
        possible_journeys = format_itineraries(journeys)
        return possible_journeys
