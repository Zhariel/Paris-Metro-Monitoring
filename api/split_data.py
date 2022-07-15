import json
import requests
import csv
import pandas as pd
import io


# -------------------- Function to flatten json files --------------- #
def flattenjson(b, delim):
    val = {}
    for i in b.keys():
        if isinstance(b[i], dict):
            get = flattenjson(b[i], delim)
            for j in get.keys():
                val[i + delim + j] = get[j]
        else:
            val[i] = b[i]

    return val


# --------------------- Function for the Itinerary ------------------ #
def get_places(lis):
    column_names = ["id", "coord", "label", "type"]
    df = pd.DataFrame(columns=column_names)
    j = 0
    for i in lis:
        coord = i["id"]
        label = i["name"]
        type_ad = i["embedded_type"]
        df2 = {'id': j, 'coord': coord, 'label': label, 'type': type_ad}
        df = df.append(df2, ignore_index=True)
        j = j + 1
    return df


# ---------------------- Function to create json for sections of a journey ------------------------------------ #
def create_sections_json(lis):
    j = 0
    sections_dict = {}
    for i in lis:
        stops = []
        if i["type"] == "public_transport":
            mode = i["display_informations"]["physical_mode"]
            for k in i["stop_date_times"]:
                stops.append(k["stop_point"]["name"])
            info = {
                "code": i["display_informations"]["code"],
                "duration": i["duration"] / 60,
                "departure_date_time": i["departure_date_time"],
                "arrival_date_time": i["arrival_date_time"],
                "from": i["from"]["stop_point"]["name"] if ("stop_point" in i["from"]) else i["from"]["stop_area"][
                    "name"] if ("stop_area" in i["from"]) else i["from"]["address"]["name"] if (
                        "address" in i["from"]) else i["from"]["name"],
                "to": i["to"]["stop_point"]["name"] if ("stop_point" in i["to"]) else i["to"]["stop_area"]["name"] if (
                        "stop_area" in i["to"]) else i["to"]["address"]["name"] if ("address" in i["to"]) else
                i["to"]["name"],
                "stops": stops
            }
            
        elif i["type"] == "street_network" or i["type"] == "crow_fly":
            mode = "walking"
            info = extract_info_street(i)

        elif i["type"] == "waiting":
            mode = "waiting"
            info = extract_info_transport(i)

        elif i["type"] == "transfer":
            mode = "transfer of transport"
            info = extract_info_street(i)

        elif i["type"] == "stay_in":
            mode = "transport"
            info = extract_info_transport(i)
        sections_dict[j] = {
            "type": i["type"],
            "mode": mode,
            "info": info
        }

        j = j + 1

    return sections_dict


def extract_info_transport(section):
    return {
        "code": "",
        "duration": section["duration"] / 60,
        "departure_date_time": section["departure_date_time"],
        "arrival_date_time": section["arrival_date_time"],
        "from": "",
        "to": "",
        "stops": []
    }


def extract_info_street(section):
    return {
        "code": "",
        "duration": section["duration"] / 60,
        "departure_date_time": section["departure_date_time"],
        "arrival_date_time": section["arrival_date_time"],
        "from": section["from"]["stop_point"]["name"] if ("stop_point" in section["from"]) else
        section["from"]["stop_area"]["name"] if ("stop_area" in section["from"]) else section["from"]["address"][
            "name"] if (
                "address" in section["from"]) else section["from"]["name"],
        "to": section["to"]["stop_point"]["name"] if ("stop_point" in section["to"]) else section["to"]["stop_area"][
            "name"] if ("stop_area" in section["to"]) else section["to"]["address"]["name"] if (
                    "address" in section["to"]) else
        section["to"]["name"],
        "stops": []
    }


# --------------------- Function for the Itinerary ------------------ #
def format_itineraries(journeys_list):
    '''
    :param journeys_list: list of journeys sent by Navitia
    :return: list of dict journeys
    '''
    # The unit of fare value is Euro
    # The unit of CO2 emission is gEC
    journeys_with_metadata = {}

    count = 0
    for itinerary in journeys_list:
        journey = {"metadata": {}}
        journey["metadata"]["nb_transfers"] = itinerary["nb_transfers"]
        journey["metadata"]["walking_duration"] = itinerary["durations"]["walking"]
        journey["metadata"]["arrival_date_time"] = itinerary["arrival_date_time"]
        journey["metadata"]["departure_date_time"] = itinerary["departure_date_time"]
        journey["metadata"]["fare_value"] = itinerary["fare"]["total"]["value"]
        journey["metadata"]["co2_emission_value"] = itinerary["co2_emission"]["value"]
        journey["metadata"]["type"] = itinerary["type"]
        journey["metadata"]["duration"] = int(itinerary["duration"]) / 60
        journey["metadata"]["nb_sections"] = len(itinerary["sections"])

        journey["sections"] = create_sections_json(itinerary["sections"])

        journeys_with_metadata[count] = journey

        count += 1
    return journeys_with_metadata

# def format_itinararies(lis):
#     # The unit of fare value is Euro
#     # The unit of CO2 emission is gEC
#     column_names = ["id", "nb_transfers", "walking_duration", "arrival_date_time", "departure_date_time", "fare_value",
#                     "co2_emission_value", "type", "duration", "nb_sections", "sections"]
#     df = pd.DataFrame(columns=column_names)
#     j = 0
#     for i in lis:
#         print("journey" + str(j))
#         id = j
#         nb_transfers = i["nb_transfers"]
#         walking_duration = i["durations"]["walking"]
#         arrival_date_time = i["arrival_date_time"]
#         departure_date_time = i["departure_date_time"]
#         fare_value = i["fare"]["total"]["value"]
#         co2_emission_value = i["co2_emission"]["value"]
#         type = i["type"]
#         duration = int(i["duration"]) / 60
#         nb_sections = len(i["sections"])
#         sections = create_sections_json(i["sections"])
#         df2 = {'id': id, 'nb_transfers': nb_transfers, 'walking_duration': walking_duration,
#                'arrival_date_time': arrival_date_time, "departure_date_time": departure_date_time,
#                "fare_value": fare_value,
#                "co2_emission_value": co2_emission_value, "type": type, "duration": duration, "nb_sections": nb_sections,
#                "sections": sections}
#         df = df.append(df2, ignore_index=True)
#         j = j + 1
#
#     return df

def get_disruptions(lis):
    
    head = 'status', 'category', 'severity_priority', 'severity_name', 'severity_effect', 'begin_date', 'end_date', 'impact_id', 'messages', 'updated_at', 'impacted_objects', 'id', 'cause'
    column_names = ['status', 'category', 'severity_priority', 'severity_name', 'severity_effect', 'begin_date', 'end_date', 'impact_id', 'messages', 'updated_at', 'impacted_objects', 'id', 'cause']
    df_disruptions = pd.DataFrame(columns=column_names)
    
    for i in lis:
        messages = ""
        for j in i["messages"]:
            messages = messages + " / " + j["text"]
        for j in i["application_periods"]:
            rawdata = []
            rawdata.append(i["status"])
            rawdata.append(i["category"])
            rawdata.append(i["severity"]["priority"])
            rawdata.append(i["severity"]["name"])
            rawdata.append(i["severity"]["effect"])
            rawdata.append(j["begin"])
            rawdata.append(j["end"])
            rawdata.append(i["impact_id"])
            rawdata.append(messages)
            rawdata.append(i["updated_at"])
            rawdata.append(i["impacted_objects"][0]["pt_object"]["name"])
            rawdata.append(i["id"])
            rawdata.append(i["cause"])
            
            df_2 = {'status' : rawdata[0], 'category' : rawdata[1], 'severity_priority' : rawdata[2], 'severity_name' : rawdata[3], 'severity_effect' : rawdata[4], 'begin_date' : rawdata[5], 'end_date' : rawdata[6], 'impact_id' : rawdata[7], 'messages' : rawdata[8], 'updated_at' : rawdata[9], 'impacted_objects' : rawdata[10], 'id' : rawdata[11], 'cause' : rawdata[12]}
            df_disruptions = df_disruptions.append(df_2, ignore_index = True)
            
    return df_disruptions


def get_lines(lis):
    new_dis = []

    for i in lis:
        new_dis.append(flattenjson(i, "__"))

    for i in new_dis:
        lis_direction_names = []
        lis_direction_ids = []
        lis_stop_areas_names = []
        lis_stop_areas_ids = []
        lis_is_frequence = []
        lis_direction_types = []
        routes = i["routes"]
        nb_routes = len(routes)

        for j in routes:
            lis_direction_names.append(j["name"])
            lis_direction_ids.append(j["id"])
            lis_stop_areas_names.append(j["direction"]["stop_area"]["name"])
            lis_stop_areas_ids.append(j["direction"]["stop_area"]["id"])
            lis_direction_types.append(j["direction_type"])
            lis_is_frequence.append(j["is_frequence"])

        i["nb_routes"] = nb_routes
        i["direction_ids"] = lis_direction_ids
        i["direction_names"] = lis_direction_names
        i["stop_areas_ids"] = lis_stop_areas_ids
        i["stop_areas_names"] = lis_stop_areas_names
        i["is_frequence"] = lis_is_frequence
        i["direction_types"] = lis_direction_types

    df_lines = pd.DataFrame.from_dict(new_dis)
    return df_lines
