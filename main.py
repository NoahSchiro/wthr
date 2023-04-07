import urllib.request
import json
import geocoder
from forecast import Forecast
import argparse

# Get request given url
def get(url):
    return urllib.request.urlopen(url)

# Decode raw bytes into JSON
def decode(response):
    return json.loads(response.read().decode('utf-8'))

# Helper function for displaying JSON
def pretty(j):
    print(json.dumps(j, indent=4))

##########################################################

def main(args):
    
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

    forecast = Forecast(g.address, response_json2, "C", args.verbose)

    print(g.address)
    forecast.print_slice(0)

# Entry point
if __name__=="__main__":

    parser = argparse.ArgumentParser(
        prog="wthr",
        description="A minimal, cross-platform weather CLI tool",

    )

    # Display more information
    parser.add_argument("-v", "--verbose", action="store_true")

    # Specify a location other than your current location
    parser.add_argument("-l", "--location")

    args = parser.parse_args()

    main(args)