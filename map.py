import  requests 
import time
currentTime = int(time.time()) #currentTime in second
startTime   =  currentTime - 3600 * 48 # 48h in the past  
username = "pdtpatrick"
password = "u3!WL2uC0dxu"
endTime = int(time.time())

URL = f"https://opensky-network.org/api/flights/departure?airport=KSEA&begin={startTime}&end={endTime}"
response = requests.get(URL, auth=(username, password)) 
data = response.json()
print(data[1])