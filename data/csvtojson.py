from pandas import *
import json
import os

stations = []
for filename in os.listdir(os.path.join('csv')):
    filename_formated = filename.replace('-', '.')
    keywords = filename_formated.split('.')
    print (filename_formated)
    # print(filename[:-4])

    csv_file = read_csv(os.path.join('csv', filename))
    # print (csv_file)
    csv_file['x'] = csv_file['x'].fillna("-")
    csv_file['y'] = csv_file['y'].fillna("-")

    x = csv_file['x'].tolist()
    y = csv_file['y'].tolist()
    # print(len(x))
    # print(len(y))

    if len(x) != len(y):
        raise Exception

    stations.append({
        "number" : keywords[0],
        "mode" : keywords[1],
        "x" : x,
        "y" : y
    })


with open('stations_list.json', 'w') as json_file:
    json.dump(stations, json_file)

