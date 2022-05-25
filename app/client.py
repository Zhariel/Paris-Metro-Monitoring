import json
import settings as se
import split_data as sd
import requests
import responses
import csv
import pandas as pd
import io

class Client:
    def __init__(self):
        self.headers = se.headers
        self.url = se.url


    def get_regions_json(self, ss = "coverage/"):
        uurl        = self.url + ss
        response    = requests.get(uurl, headers=self.headers).json()
        #df          = pd.DataFrame(response)
        #print(df)
        #df.to_csv(r'C:\Users\ASUS\Documents\M2\projet_annuel\Paris-Metro-Monitoring\data\navitia\regions.csv', index=None)
        #print(response.json())

    def get_all_disruptions_json(self, ss = "disruptions/"):
        uurl = self.url + ss
        response = requests.get(uurl, headers=self.headers)

    def get_all_stop_areas_json(self, ss = "stop_areas/"):
        uurl = self.url + ss
        response = requests.get(uurl, headers=self.headers)

    def get_all_lines_json(self, ss = "lines/"):
        uurl = self.url + ss
        response = requests.get(uurl, headers=self.headers)

    def get_all_Metro_lines_json(self, ss = "coverage/fr-idf/physical_modes/physical_mode:Metro/lines"):
        uurl            = self.url + ss
        responsee       = requests.get(uurl, headers=self.headers).json()
        disruptions     = responsee["disruptions"]
        lines           = responsee["lines"]
        new_lin         = []
        df_dispuptions  =  sd.get_disruptions(disruptions)
        df_dispuptions.to_csv("../data/navitia/metros/disruptions_metros.csv",index=False, sep=';')

    def get_all_Bus_lines_json(self, ss = "coverage/fr-idf/physical_modes/physical_mode:Bus/lines"):
        uurl            = self.url + ss
        responsee       = requests.get(uurl, headers=self.headers).json()
        disruptions     = responsee["disruptions"]
        lines           = responsee["lines"]
        new_lin         = []
        df_dispuptions  =  sd.get_disruptions(disruptions)
        df_dispuptions.to_csv("../data/navitia/bus/disruptions_bus.csv",index=False, sep=';')

    def get_all_Tramway_lines_json(self, ss = "coverage/fr-idf/physical_modes/physical_mode:Tramway/lines"):
        uurl            = self.url + ss
        responsee       = requests.get(uurl, headers=self.headers).json()
        disruptions     = responsee["disruptions"]
        lines           = responsee["lines"]
        new_lin         = []
        df_dispuptions  =  sd.get_disruptions(disruptions)
        df_dispuptions.to_csv("../data/navitia/tramways/disruptions_tram.csv",index=False, sep=';')


    def get_all_LocalTrains_lines_json(self, ss = "coverage/fr-idf/physical_modes/physical_mode:LocalTrain/lines"):
        uurl            = self.url + ss
        responsee       = requests.get(uurl, headers=self.headers).json()
        disruptions     = responsee["disruptions"]
        lines           = responsee["lines"]
        new_lin         = []
        df_dispuptions  =  sd.get_disruptions(disruptions)
        df_dispuptions.to_csv("../data/navitia/localtrains/disruptions_localtrains.csv",index=False, sep=';')


    def get_all_RapidTransit_lines_json(self, ss = "coverage/fr-idf/physical_modes/physical_mode:RapidTransit/lines"):
        uurl            = self.url + ss
        responsee       = requests.get(uurl, headers=self.headers).json()
        disruptions     = responsee["disruptions"]
        lines           = responsee["lines"]
        new_lin         = []
        df_dispuptions  =  sd.get_disruptions(disruptions)
        df_dispuptions.to_csv("../data/navitia/rapidtransits/disruptions_rapidtransit.csv",index=False, sep=';')


    # Get all close points
    def get_all_pois_json(self, ss = "pois/"):
        uurl = self.url + ss
        response = requests.get(uurl, headers=self.headers)

    def get_all_poi_types_json(self, ss = "poi_types/"):
        uurl = self.url + ss
        response = requests.get(uurl, headers=self.headers)









safa = Client()
safa.get_all_Metro_lines_json()
safa.get_all_Bus_lines_json()
safa.get_all_Tramway_lines_json()
safa.get_all_LocalTrains_lines_json()
safa.get_all_RapidTransit_lines_json()
