import json
#from api import *
from settings import *
import split_data as data_utils
import requests
import csv
import pandas as pd
import io

class Itinerary:

    def __init__(self):
        self.headers = HEADERS
        self.url = URL

    def send_request(self, arg):
        uurl            = self.url + "coverage/fr-idf/" + arg
        response        = requests.get(uurl, headers=self.headers).json()

        return response

    def get_address(self, addr):
        arg                 = "places?q=" + addr
        response            = self.send_request(arg)
        places              = response["places"]
        possible_addresses  = data_utils.get_places(places)

iti = Itinerary()
iti.get_address("rue perthuis")
