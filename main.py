import urllib.request
import json
import geocoder
from forecast import Forecast

# Get request given url
def get(url):
    return urllib.request.urlopen(url)

def decode(response):
    return json.loads(response.read().decode('utf-8'))

# Helper function for displaying JSON
def pretty(j):
    print(json.dumps(j, indent=4))

##########################################################

# Get location
g = geocoder.ip('me')

# Break this down into latitude and longitude
lat,lon = g.latlng

# First request is going to determine what weather station we need to query
location_query_url = f"https://api.weather.gov/points/{lat},{lon}"
r1 = get(location_query_url)
response_json1 = decode(r1)

# Forecast_query_url is going to store the
# url we actually need to query for our data
forecast_query_url = response_json1["properties"]["forecast"] + "/hourly"
r2 = get(forecast_query_url)
response_json2 = decode(r2)

#pretty(response_json2["properties"]["periods"][0])

forecast = Forecast(g.address, response_json2, "C")

print(g.address)
print(forecast.time_slices[0])