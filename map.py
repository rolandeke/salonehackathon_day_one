import requests
from requests.exceptions import HTTPError
import typing 
import time
from typing import Dict
import csv
import json

username = "pdtpatrick"
password = "u3!WL2uC0dxu"
current_time = int(time.time())
start_time = current_time - (3600 * 48)
end_time = current_time
airport = "KSEA"

def get_data_from_api(airport:str,start_time:int,end_time:int):
    """
        Function calls to the API for all arrival flights at a particular Airport 
        @params airport
        @params start_time
        @params end_time
        
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

   
   
def get_coordinates(start:int, end:int):
    outputData = []
    flights = get_data_from_api(airport,start,end)
    airports_from_csv = read_from_csv("airports.csv")
    
    #looping through all flights returned by the api
    for arrivals in flights:
        #get the airport names and store in variables
        departureAirport = arrivals['estDepartureAirport']
        arrivalAirport = arrivals['estArrivalAirport']
        
        #get latitude and long of departure airport from dict returned by csv
        if departureAirport  in airports_from_csv:
            dept_lat = airports_from_csv[departureAirport]['latitude']
            dept_lon = airports_from_csv[departureAirport]['longitude']
            
        if arrivalAirport in airports_from_csv:
            arr_lat = airports_from_csv[arrivalAirport]['latitude']
            arr_lon = airports_from_csv[arrivalAirport]['longitude']
            
        outputData.append({
            "deptLat" : dept_lat,
            "deptLon" : dept_lon,
            "arrLon" : arr_lon,
            "arr_lat" : arr_lat 
        })
        
        return json.dumps(outputData)
        
            

flights = get_data_from_api("KSEA",start_time,end_time)

print(len(flights))

    
    