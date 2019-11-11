import requests
from requests.exceptions import HTTPError
import typing 
import time
from typing import Dict

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
    

   
def get_coordinates(start:int, end:int):
    outputData = []
    flights = get_data_from_api(airport,start,end)
    airports_from_csv = read_from_csv("airports.csv")
            

flights = get_data_from_api("KSEA",start_time,end_time)

print(len(flights))

    
    