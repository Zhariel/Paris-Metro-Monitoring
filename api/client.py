import json
from api import *
import split_data as data_utils
import requests
import csv
import pandas as pd
import io

class Client:
    def __init__(self):
        self.headers = HEADERS
        self.url = URL


    def get_regions_json(self, suffix = "coverage/"):
        uurl        = self.url + suffix
        response    = requests.get(uurl, headers=self.headers).json()
        #df          = pd.DataFrame(response)
        #print(df)
        #df.to_csv(r'C:\Users\ASUS\Documents\M2\projet_annuel\Paris-Metro-Monitoring\data\navitia\regions.csv', index=None)
        #print(response.json())

    def get_all_disruptions_json(self, suffix = "disruptions/"):
        uurl = self.url + suffix
        response = requests.get(uurl, headers=self.headers)

    def get_all_stop_areas_json(self, suffix = "stop_areas/"):
        uurl = self.url + suffix
        response = requests.get(uurl, headers=self.headers)

    def get_all_lines_json(self, suffix = "lines/"):
        uurl = self.url + suffix
        response = requests.get(uurl, headers=self.headers)

    def get_all_Metro_lines_json(self, suffix = "coverage/fr-idf/physical_modes/physical_mode:Metro/lines"):
        uurl            = self.url + suffix
        response        = requests.get(uurl, headers=self.headers).json()
        disruptions     = response["disruptions"]
        lines           = response["lines"]
        new_lin         = []
        df_dispuptions  =  data_utils.get_disruptions(disruptions)
        df_dispuptions.to_csv("../data/navitia/metros/disruptions_metros.csv",index=False, sep=';')

    def get_all_Bus_lines_json(self, suffix = "coverage/fr-idf/physical_modes/physical_mode:Bus/lines"):
        uurl            = self.url + suffix
        response        = requests.get(uurl, headers=self.headers).json()
        disruptions     = response["disruptions"]
        lines           = response["lines"]
        new_lin         = []
        df_dispuptions  =  data_utils.get_disruptions(disruptions)
        df_dispuptions.to_csv("../data/navitia/bus/disruptions_bus.csv",index=False, sep=';')

    def get_all_Tramway_lines_json(self, suffix = "coverage/fr-idf/physical_modes/physical_mode:Tramway/lines"):
        uurl            = self.url + suffix
        response        = requests.get(uurl, headers=self.headers).json()
        disruptions     = response["disruptions"]
        lines           = response["lines"]
        new_lin         = []
        df_dispuptions  =  data_utils.get_disruptions(disruptions)
        df_dispuptions.to_csv("../data/navitia/tramways/disruptions_tram.csv",index=False, sep=';')


    def get_all_LocalTrains_lines_json(self, suffix = "coverage/fr-idf/physical_modes/physical_mode:LocalTrain/lines"):
        uurl            = self.url + suffix
        response        = requests.get(uurl, headers=self.headers).json()
        disruptions     = response["disruptions"]
        lines           = response["lines"]
        new_lin         = []
        df_dispuptions  =  data_utils.get_disruptions(disruptions)
        df_dispuptions.to_csv("../data/navitia/localtrains/disruptions_localtrains.csv",index=False, sep=';')


    def get_all_RapidTransit_lines_json(self, suffix = "coverage/fr-idf/physical_modes/physical_mode:RapidTransit/lines"):
        uurl            = self.url + suffix
        response       = requests.get(uurl, headers=self.headers).json()
        disruptions     = response["disruptions"]
        lines           = response["lines"]
        new_lin         = []
        df_dispuptions  =  data_utils.get_disruptions(disruptions)
        df_dispuptions.to_csv("../data/navitia/rapidtransits/disruptions_rapidtransit.csv",index=False, sep=';')


    # Get all close points
    def get_all_pois_json(self, suffix = "pois/"):
        uurl = self.url + suffix
        response = requests.get(uurl, headers=self.headers)

    def get_all_poi_types_json(self, suffix = "poi_types/"):
        uurl = self.url + suffix
        response = requests.get(uurl, headers=self.headers)









client = Client()
client.get_all_Metro_lines_json()
client.get_all_Bus_lines_json()
client.get_all_Tramway_lines_json()
client.get_all_LocalTrains_lines_json()
client.get_all_RapidTransit_lines_json()
