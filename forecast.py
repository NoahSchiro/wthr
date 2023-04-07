class Forecast():

    def __init__(self, location, json, preferredUnit, verbose=False):

        self.verbose = verbose
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

    def print_slice(self, slice_num):

        slice = self.time_slices[slice_num]

        # Determine what unit to print
        temp = None

        if self.preferredUnit == "F":
            temp = slice["temp"]
        else:
            temp = (slice["temp"] - 32) * (5/9)

        # Unicode for degree symbol
        degree_sym = "\u00B0"

        s = None

        if self.verbose:
            s = "Verbosity not yet implemented"
        else:
            s = f"""
{slice["startDate"]}, {slice["startTime"]}:
Temperature:      {temp:.1f}{degree_sym}{self.preferredUnit}
Precipitation %:  {slice["prob"]}%
Windspeed:        {slice["windSpeed"]} {slice["windDirection"]}"""

        print(s)