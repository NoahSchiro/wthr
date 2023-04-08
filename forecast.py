class Forecast():

    def __init__(self, location, json, preferredUnit, args):

        self.forecast = args.forecast
        self.location = location
        self.raw = json
        self.preferredMeasurements = preferredUnit

        self.time_slices = []

        self._parse(self.raw)
 
    def _parse(self, json):
            
        # The data is split into hourly time slices. Grab those
        periods = json["properties"]["periods"]

        for period in periods:

            # Time info
            startDate, startTimeRaw = period["startTime"].split("T")
            startTime = startTimeRaw[:5]

            # Temp info
            temp     = period["temperature"]
            tempUnit = period["temperatureUnit"]

            # Wind speed and direction
            windSpeed = period["windSpeed"].split(" ")[0]
            windDirection = period["windDirection"]

            # Probability of precipitation
            prob = period["probabilityOfPrecipitation"]["value"]

            # Short description in english prose
            shortProse = period["shortForecast"]

            obj = {
                "startDate": startDate,
                "startTime": startTime,
                "temp": self._get_temp(temp),
                "tempUnit": tempUnit,
                "windSpeed": self._get_speed(windSpeed),
                "windDirection": self._get_direction(windDirection),
                "prob": prob,
                "shortProse": shortProse 
            }

            self.time_slices.append(obj)

    def _get_temp(self, temp_value):

        # Unicode for degree symbol
        degree_sym = "\u00B0"

        if self.preferredMeasurements == "imperial":
            return str(temp_value) + degree_sym +  "F"
        else:
            value = f"{(temp_value - 32) * (5/9):.1f}"
            return value + degree_sym +  "C"
        
    def _get_speed(self, speed):

        if self.preferredMeasurements == "imperial":
            return speed + "mph"
        else:
            value = f"{float(speed) * 1.6093:.1f}"
            return value + "kmh"
        
    def _get_direction(self, direction):

        if direction == "N":
            return "\u2191"
        elif direction == "NE":
            return "\u2197"
        elif direction == "E":
            return "\u2192"
        elif direction == "SE":
            return "\u2198"
        elif direction == "S":
            return "\u2193"
        elif direction == "SW":
            return "\u2199"
        elif direction == "W":
            return "\u2190"
        elif direction == "NW":
            return "\u2196"
        else:
            print(f"Error! Unrecognized direction {direction}")
            
    def print_slice(self):

        # Print information about the future
        if self.forecast:

            for i in range(12):

                # Get slice
                slice = self.time_slices[i]
                
                s = f"""
{slice["startDate"]}, {slice["startTime"]}:
    Temperature:      {slice["temp"]}
    Precipitation %:  {slice["prob"]}%
    Windspeed:        {slice["windSpeed"]} {slice["windDirection"]}"""

                print(s)

        # Default case
        else:

            # Get the most current slice
            slice = self.time_slices[0]

            s = f"""
{slice["startDate"]}, {slice["startTime"]}:
    {slice["shortProse"]}
    Temperature:      {slice["temp"]}
    Precipitation %:  {slice["prob"]}%
    Windspeed:        {slice["windSpeed"]} {slice["windDirection"]}"""

            print(s)