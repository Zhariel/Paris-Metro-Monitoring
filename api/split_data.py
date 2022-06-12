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
    column_names    = ["id", "coord", "label", "lat", "lon"]
    df              = pd.DataFrame(columns = column_names)
    j               = 0
    for i in lis:
        coord       = i["id"]
        label       = i["name"]
        lat         = i["address"]["coord"]["lat"]
        lon         = i["address"]["coord"]["lon"]
        df2         = {'id': j, 'coord': coord, 'label': label, 'lat' : lat, 'lon' : lon}
        df          = df.append(df2, ignore_index = True)
        j           = j + 1
    return df



def get_disruptions(lis):
    new_dis         = []

    for i in lis:
        new_dis.append(flattenjson(i, "__"))

    for i in new_dis:
        lis_mes             = []
        lis_embed_types     = []
        lis_line_codes      = []
        lis_line_names      = []
        lis_line_phys       = []
        lis_commercial_mode = []
        lis_stop_values     = []
        lis_stop_names      = []
        lis_stop_labels     = []
        #pt_object           = i['impacted_objects'][0]['pt_object']
        pt_object           = i['impacted_objects']
        for j in pt_object:
            lis_embed_types.append(j['pt_object']['embedded_type'])
            try:
                line        = j['pt_object']['line']
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
                stop_area       = j['pt_object']['stop_area']
                lis_stop_values.append(stop_area['codes'][0]['value'])
                lis_stop_names.append(stop_area['name'])
                lis_stop_labels.append(stop_area['label'])
            except:
                lis_stop_values.append("")
                lis_stop_names.append("")
                lis_stop_labels.append("")

        i['embedded_type']       = lis_embed_types
        i['line_code']           = lis_line_codes
        i['line_name']           = lis_line_names
        i['line_physical_mode']  = lis_line_phys
        i['line_commecial_mode'] = lis_commercial_mode
        i['stop_area_value']     = lis_stop_values
        i['stop_area_name']      = lis_stop_names
        i['stop_area_label']     = lis_stop_labels

        messages            = i["messages"]
        for j in messages:
            lis_mes.append(j["text"])
        i["messages"] = lis_mes

    df_dispuptions  = pd.DataFrame.from_dict(new_dis)
    return df_dispuptions


def get_lines(lis):
    new_dis         = []

    for i in lis:
        new_dis.append(flattenjson(i, "__"))


    for i in new_dis:
        lis_direction_names           = []
        lis_direction_ids             = []
        lis_stop_areas_names          = []
        lis_stop_areas_ids            = []
        lis_is_frequence              = []
        lis_direction_types           = []
        routes                        = i["routes"]
        nb_routes                     = len(routes)

        for j in routes:
             lis_direction_names.append(j["name"])
             lis_direction_ids.append(j["id"])
             lis_stop_areas_names.append(j["direction"]["stop_area"]["name"])
             lis_stop_areas_ids.append(j["direction"]["stop_area"]["id"])
             lis_direction_types.append(j["direction_type"])
             lis_is_frequence.append(j["is_frequence"])

        i["nb_routes"]              = nb_routes
        i["direction_ids"]          = lis_direction_ids
        i["direction_names"]        = lis_direction_names
        i["stop_areas_ids"]         = lis_stop_areas_ids
        i["stop_areas_names"]       = lis_stop_areas_names
        i["is_frequence"]           = lis_is_frequence
        i["direction_types"]        = lis_direction_types

    df_lines  = pd.DataFrame.from_dict(new_dis)
    return df_lines
