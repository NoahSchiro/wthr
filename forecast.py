class Forecast():

    def __init__(self, location, json, preferredUnit, args):

        self.verbose = args.verbose
        self.forecast = args.forecast
        self.location = location
        self.raw = json
        self.preferredUnit = preferredUnit

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
            windSpeed = period["windSpeed"].replace(" ", "")
            windDirection = period["windDirection"]

            # Probability of precipitation
            prob = period["probabilityOfPrecipitation"]["value"]

            # Short description in english prose
            shortProse = period["shortForecast"]

            obj = {
                "startDate": startDate,
                "startTime": startTime,
                "temp": temp,
                "tempUnit": tempUnit,
                "windSpeed": windSpeed,
                "windDirection": windDirection,
                "prob": prob,
                "shortProse": shortProse 
            }

            self.time_slices.append(obj)

    def _get_temp(self, temp_value):

        if self.preferredUnit == "F":
            return temp_value
        else:
            return (temp_value - 32) * (5/9)
        
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

        # Unicode for degree symbol
        degree_sym = "\u00B0"

        # Print verbose information about the weather
        if self.verbose:
            s = "Verbosity not yet implemented"

        # Print information about the future
        elif self.forecast:

            for i in range(12):

                # Get slice
                slice = self.time_slices[i]

                # Determine temp
                temp = self._get_temp(slice["temp"])

                s = f"""
{slice["startDate"]}, {slice["startTime"]}:
    Temperature:      {temp:.1f}{degree_sym}{self.preferredUnit}
    Precipitation %:  {slice["prob"]}%
    Windspeed:        {slice["windSpeed"]} {self._get_direction(slice["windDirection"])}"""

                print(s)

        # Default case
        else:

            # Get the most current slice
            slice = self.time_slices[0]

            # Determine what unit to print
            temp = self._get_temp(slice["temp"])

            s = f"""
{slice["startDate"]}, {slice["startTime"]}:
    Temperature:      {temp:.1f}{degree_sym}{self.preferredUnit}
    Precipitation %:  {slice["prob"]}%
    Windspeed:        {slice["windSpeed"]} {self._get_direction(slice["windDirection"])}"""

            print(s)