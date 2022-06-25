import json
#from api import *
from settings import *
import split_data as data_utils
import requests
import csv
import pandas as pd
import io

class Client:
    def __init__(self):
        self.headers = HEADERS
        self.url = URL


    def factor_data(self, transportMode):
        uurl            = self.url + "coverage/fr-idf/physical_modes/physical_mode:" + transportMode + "/lines"
        response        = requests.get(uurl, headers=self.headers).json()
        disruptions     = response["disruptions"]
        lines           = response["lines"]
        df_dispuptions  = data_utils.get_disruptions(disruptions)
        df_lines        = data_utils.get_lines(lines)

        return df_dispuptions, df_lines

    def df_to_csv(self, df_dispuptions, df_lines, disruptions_file, lines_file):
        path                = "../data/navitia/"
        disruptions_path    = path + disruptions_file
        lines_path          = path + lines_file
        df_dispuptions.to_csv(disruptions_path,index=False, sep=';')
        df_lines.to_csv(lines_path,index=False, sep=';')

    def get_all_Metro_lines_json(self):
        df_dispuptions, df_lines = self.factor_data("Metro")
        self.df_to_csv(df_dispuptions, df_lines,"metros/disruptions_metros.csv","metros/lines_metros.csv")

    def get_all_Bus_lines_json(self):
        df_dispuptions, df_lines = self.factor_data("Bus")
        self.df_to_csv(df_dispuptions, df_lines,"bus/disruptions_bus.csv","bus/lines_bus.csv")

    def get_all_Tramway_lines_json(self):
        df_dispuptions, df_lines = self.factor_data("Tramway")
        self.df_to_csv(df_dispuptions, df_lines,"tramways/disruptions_tram.csv","tramways/lines_tramways.csv")


    def get_all_LocalTrains_lines_json(self):
        df_dispuptions, df_lines = self.factor_data("LocalTrain")
        self.df_to_csv(df_dispuptions, df_lines,"localtrains/disruptions_localtrains.csv","localtrains/lines_localtrains.csv")


    def get_all_RapidTransit_lines_json(self):
        df_dispuptions, df_lines = self.factor_data("RapidTransit")
        self.df_to_csv(df_dispuptions, df_lines,"rapidtransits/disruptions_rapidtransit.csv","rapidtransits/lines_rapidtransits.csv")


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
