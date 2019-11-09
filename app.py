##python 
import time
from typing import Dict 
import requests
import logging
import pprint
import typing
import csv

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

currentTime = int(time.time()) #currentTime in second
startTime   =  currentTime - 3600 * 48 # 48h in the past  
username = "pdtpatrick"
password = "u3!WL2uC0dxu"

def call_api(airport,startTime,endTime):
    """Call opensky API and return all departures

    begin = now - days ago
    end = now
    """
    time.sleep(10)
    URL = f"https://opensky-network.org/api/flights/departure?airport={airport}&begin={startTime}&end={endTime}"
    logging.info(f"URL is now: {URL}")
    r = requests.get(URL, auth=(username, password))
    if r.status_code == 404:
        logging.error("Cannot find data")
        return None
    assert len(r.json()) != 0
    return r.json()

# departures = call_api("KSEA",startTime,currentTime)

# pprint.pprint(departures[1])
def read_airport(filename: str) -> Dict[str, str]:
    keys  =  ["id","name","city","country","IATA","ICAO",
             "latitude","longitude","altitude","timezone",
             "dst","tz","type","source"]
    airports  = [a for a in csv.DictReader(open(filename,encoding='utf-8'),delimiter=',',quotechar='"',fieldnames=keys)]
    return airports #[15:25]

airports = read_airport("airports.csv")

lat = airports[0]['latitude']
lon = airports[0]['longitude']

