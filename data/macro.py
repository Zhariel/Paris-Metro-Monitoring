
import requests
from bs4 import BeautifulSoup
from lxml import html

url = "https://parispass.com/en-us/paris-transport/metro-map"

response = requests.get(url)

soup = BeautifulSoup(response.text, "lxml")

lis = []
for row in soup.select('tbody tr'):
    lis.append([x.text for x in row.find_all('td')])

lis[0] = ['Station', 'Line', 'Zone']

with open("stations.csv", "w") as stations:
    for f in lis:
        new = [e.replace(',', '/').replace('&', '/') for e in f]
        if len(new) < 3:
            continue
        new[1] = new[1].replace(' ', '')
        new[2] = new[2].replace(' ', '')
        stations.write(','.join(new) + '\n')

