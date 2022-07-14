from ast import arg
import json
from platform import python_branch
# from api import *
from settings import HEADERS, URL_BASE, LINES_ENDPOINT, JOURNEYS_ENDPOINT
import split_data as data_utils
import requests
import csv
import pandas as pd
import io


class Itinerary:

    def __init__(self, departure, destination):
        self.headers = HEADERS
        self.url_base = URL_BASE
        self.departure = departure
        self.destination = destination

    def send_request(self, arg):
        uurl = self.url_base + arg
        response = requests.get(uurl, headers=self.headers).json()

        return response

    def get_address(self, addr):
        arg = "places?q=" + addr
        response = self.send_request(arg)
        places = response["places"]
        possible_addresses = data_utils.get_places(places)
        return possible_addresses

    def get_itineraries(self):
        departure = self.departure
        destination = self.destination
        id_departure = self.get_address(departure).iloc[0]["coord"]
        print(id_departure)
        id_destination = self.get_address(destination).iloc[0]["coord"]
        print(id_destination)

        arg = "journeys?from=" + id_departure + "&to=" + id_destination 
        response = self.send_request(arg)
        journeys = response["journeys"]
        possible_journeys = data_utils.format_itinararies(journeys)
        return possible_journeys
