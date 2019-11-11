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
airport = "KSEA"

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

   
   
# def get_coordinates(start:int, end:int):
#     outputData = []
#     flights = get_data_from_api(airport,start,end)
#     airports_from_csv = read_from_csv("airports.csv")
    
#     #looping through all flights returned by the api
#     for arrivals in flights:
#         #get the airport names and store in variables
#         departureAirport = arrivals['estDepartureAirport']
#         arrivalAirport = arrivals['estArrivalAirport']
        
#         #get latitude and long of departure airport from dict returned by csv
#         if departureAirport  in airports_from_csv:
#             dept_lat = airports_from_csv[departureAirport]['latitude']
#             dept_lon = airports_from_csv[departureAirport]['longitude']
            
#         if arrivalAirport in airports_from_csv:
#             arr_lat = airports_from_csv[arrivalAirport]['latitude']
#             arr_lon = airports_from_csv[arrivalAirport]['longitude']
            
#         outputData.append({
#             "deptLat" : dept_lat,
#             "deptLon" : dept_lon,
#             "arrLon" : arr_lon,
#             "arr_lat" : arr_lat 
#         })
        
#         return outputData

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
    
    
cords = get_coordinates(start_time, end_time)



def draw_map(coordinates:list):
   
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])
    m = Basemap(\
                rsphere=(6378137.00,6356752.3142),\
                resolution='l',projection='cyl',\
                lat_0=40.,lon_0=-20.,lat_ts=20.)
    
    deplon = float(coordinates[10]['depLon'])
    deplat = float(coordinates[10]['depLat'])
    arrlon = float(coordinates[10]['arrLon'])
    arrlat = float(coordinates[10]['arrLat'])
    # nylat = 40.78; nylon = -73.98
    # # lonlat, lonlon are lat/lon of London.
    # lonlat = 51.53; lonlon = 0.08
    # # draw great circle route between NY and London
    m.drawgreatcircle(deplon,deplat,arrlon,arrlat,linewidth=2,color='b')
    m.drawcoastlines()
    m.fillcontinents()
    # draw parallels
    m.drawparallels(np.arange(10,90,20),labels=[1,1,0,1])
    # draw meridians
    m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])
    ax.set_title('Flight Movement Map')
    plt.show()


draw_map(cords)