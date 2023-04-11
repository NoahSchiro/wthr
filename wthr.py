#!/usr/bin/env python3

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

    # Load in configurations
    config = json.load(open("config.json"))
    preferredSystem = config["preferredSystem"]

    lat, lon = None, None
    address = None

    # Get location
    # TODO: Handle the case where there is no internet connection
    g = geocoder.ip('me')

    if args.location != None:
        query = config["locations"][args.location]
        lat, lon = query["lat"], query["lon"]
        address = query["address"]
    else:
        lat,lon = g.latlng
        address = g.address

    if args.save:
        locationName = g.city.replace(" ", "")
        config["locations"][locationName] = {}

        config["locations"][locationName]["address"] = address
        config["locations"][locationName]["lat"] = lat
        config["locations"][locationName]["lon"] = lon
        json.dump(config, open("config.json", "w"), indent=4)

    
    # First request is going to determine what weather station we need to query
    # TODO: Handle the case where there is no internet connection
    location_query_url = f"https://api.weather.gov/points/{lat},{lon}"
    r1 = get(location_query_url)
    response_json1 = decode(r1)

    # Forecast_query_url is going to store the
    # url we actually need to query for our data
    # TODO: Handle the case where there is no internet connection
    forecast_query_url = response_json1["properties"]["forecast"] + "/hourly"
    r2 = get(forecast_query_url)
    response_json2 = decode(r2)

    # Store all of our data in a nice way
    forecast = Forecast(address, response_json2, preferredSystem, args)

    # Show data
    # TODO: Maybe add color and some other cool TUI effects
    print(address)
    forecast.print_slice()

# Entry point
if __name__=="__main__":

    parser = argparse.ArgumentParser(
        prog="wthr",
        description="A minimal, cross-platform weather CLI tool",
    )
   
    parser.add_argument("-s", "--save",
        action="store_true",
        help="Save your current location to a config file for future lookup")

    # Specify a location other than your current location
    parser.add_argument("-l", "--location",
        help="Choose another location to query")
    
    parser.add_argument("-f", "--forecast",
        action="store_true",
        help="See the 12 hour forecast for the location")

    args = parser.parse_args()

    main(args)
