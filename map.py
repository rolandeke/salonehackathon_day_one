import requests
from requests.exceptions import HTTPError
import typing 
import time
from typing import Dict
from typing import List 
import csv
import json
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt


username = "pdtpatrick"
password = "u3!WL2uC0dxu"
current_time = int(time.time())
start_time = current_time - (3600 * 48)
end_time = current_time
airport = "EDDF"

def get_data_from_api(airport:str,start_time:int,end_time:int):
    """
        Function calls to the API for all arrival flights at a particular Airport 
        :params airport
        :params start_time
        :params end_time
        
        returns response_from_api
    """
    #connect to the api
    URL = f"https://opensky-network.org/api/flights/arrival?airport={airport}&begin={start_time}&end={end_time}"
    try:
        response_from_api = requests.get(URL,auth=(username,password))
        response_from_api.raise_for_status()
    except HTTPError as error:
        print(error)
    else:
        if response_from_api.status_code == 200:
            assert len(response_from_api.json()) != 0
            return response_from_api.json()
        elif response_from_api.status_code == 404:
            print("Data Not Found")
            return None

def read_from_csv(filename:str):
        keys = [
        "id",
        "name",
        "city",
        "country",
        "IATA",
        "ICAO",
        "latitude",
        "longitude",
        "altitude",
        "timezone",
        "dst",
        "tz",
        "type",
        "source",
    ]
        airports = csv.DictReader(
            open(filename,encoding="utf-8"), delimiter=",", quotechar='"', fieldnames=keys
        )
        d = {airport["ICAO"]: airport for airport in airports}
        return d

   

def get_coordinates(st:int ,en:int) -> List[Dict[str , str]]:
    
    outputData = []
    csvData = read_from_csv('airports.csv')
    airData = get_data_from_api(airport,st,en)
    arr_lat = csvData[airport]['latitude']
    arr_lon = csvData[airport]['longitude']
    
    for flight in get_data_from_api(airport,st,en):
        dept_air = flight['estDepartureAirport']
        if dept_air in csvData:
            dep_lat = csvData[dept_air]['latitude']
            dep_lon = csvData[dept_air]['longitude']
        
        outputdict = { 
                        "arrLat" : arr_lat,
                        "depLat": dep_lat, 
                        "arrLon" : arr_lon,
                        "depLon" : dep_lon 
                    }
        outputData.append(outputdict)
        
    return outputData
    

def draw_map(coordinates:list):
    
    """
        This function draws a map for a list of 
        Coordinates that would be passed as a parameter
        The function loops through the list of 
        coordinates and then plots the map for every departure airport from the 
        arrival airport.
        :params List[Dict[str,str]]
    """
   
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])
    m = Basemap(\
                rsphere=(6378137.00,6356752.3142),\
                resolution='l',projection='cyl',\
                )
    arrlon = float(coordinates[0]['arrLon'])
    arrlat = float(coordinates[0]['arrLat'])
    
    for i in range(len(coordinates)):
        deplon = float(coordinates[i]['depLon'])
        deplat = float(coordinates[i]['depLat'])
        # # draw great circle route between Arrival and Department Airport
        m.drawgreatcircle(deplon,deplat,arrlon,arrlat,linewidth=1,color='r')
        m.plot(deplon,deplat, marker='o',color='b')
        
        
    m.drawcoastlines()
    m.fillcontinents()
    m.drawmapboundary(fill_color='aqua')
    #draw parallels
    m.drawparallels(np.arange(10,90,20),labels=[1,1,0,1])
    #draw meridians
    m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])
    ax.set_title('Flight Movement Map From EDDF Airport By Chinedum Roland Eke')
    plt.show()
    
    

cords = get_coordinates(start_time, end_time)
draw_map(cords)