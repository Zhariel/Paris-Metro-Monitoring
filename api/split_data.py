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
        print("section " + str(j))
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
def format_itinararies(lis):
    # The unit of fare value is Euro
    # The unit of CO2 emission is gEC
    column_names = ["id", "nb_transfers", "walking_duration", "arrival_date_time", "departure_date_time", "fare_value",
                    "co2_emission_value", "type", "duration", "nb_sections", "sections"]
    df = pd.DataFrame(columns=column_names)
    j = 0
    for i in lis:
        print("journey" + str(j))
        id = j
        nb_transfers = i["nb_transfers"]
        walking_duration = i["durations"]["walking"]
        arrival_date_time = i["arrival_date_time"]
        departure_date_time = i["departure_date_time"]
        fare_value = i["fare"]["total"]["value"]
        co2_emission_value = i["co2_emission"]["value"]
        type = i["type"]
        duration = int(i["duration"]) / 60
        nb_sections = len(i["sections"])
        sections = create_sections_json(i["sections"])
        df2 = {'id': id, 'nb_transfers': nb_transfers, 'walking_duration': walking_duration,
               'arrival_date_time': arrival_date_time, "departure_date_time": departure_date_time,
               "fare_value": fare_value,
               "co2_emission_value": co2_emission_value, "type": type, "duration": duration, "nb_sections": nb_sections,
               "sections": sections}
        df = df.append(df2, ignore_index=True)
        j = j + 1

    return df


def get_disruptions(lis):
    new_dis = []

    for i in lis:
        new_dis.append(flattenjson(i, "__"))

    for i in new_dis:
        lis_mes = []
        lis_embed_types = []
        lis_line_codes = []
        lis_line_names = []
        lis_line_phys = []
        lis_commercial_mode = []
        lis_stop_values = []
        lis_stop_names = []
        lis_stop_labels = []
        # pt_object           = i['impacted_objects'][0]['pt_object']
        pt_object = i['impacted_objects']
        for j in pt_object:
            lis_embed_types.append(j['pt_object']['embedded_type'])
            try:
                line = j['pt_object']['line']
                lis_line_codes.append(line['code'])
                lis_line_names.append(line['name'])
                lis_line_phys.append(line['physical_modes'])
                lis_commercial_mode.append(line['lis_commercial_mode']['name'])
            except:
                lis_line_codes.append("")
                lis_line_names.append("")
                lis_line_phys.append("")
                lis_commercial_mode.append("")

            try:
                stop_area = j['pt_object']['stop_area']
                lis_stop_values.append(stop_area['codes'][0]['value'])
                lis_stop_names.append(stop_area['name'])
                lis_stop_labels.append(stop_area['label'])
            except:
                lis_stop_values.append("")
                lis_stop_names.append("")
                lis_stop_labels.append("")

        i['embedded_type'] = lis_embed_types
        i['line_code'] = lis_line_codes
        i['line_name'] = lis_line_names
        i['line_physical_mode'] = lis_line_phys
        i['line_commecial_mode'] = lis_commercial_mode
        i['stop_area_value'] = lis_stop_values
        i['stop_area_name'] = lis_stop_names
        i['stop_area_label'] = lis_stop_labels

        messages = i["messages"]
        for j in messages:
            lis_mes.append(j["text"])
        i["messages"] = lis_mes

    df_disruptions = pd.DataFrame.from_dict(new_dis)
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
