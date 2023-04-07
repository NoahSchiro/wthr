
class Slice():

    def __init__(self, date, time, temp, tempUnit, preferredUnit, windSpeed, windDirection, prob, shortProse):
        self.date = date
        self.time = time


        self.tempF = None
        self.tempC = None
        self.preferredUnit = preferredUnit
        if tempUnit == "F":
            self.tempF = float(temp)
            self.tempC = float((temp - 32) * (5/9))
        else:
            self.tempF = float(temp * (9/5) + 32)
            self.tempC = float(temp)

        self.windSpeed = windSpeed
        self.windDirection = windDirection
        self.prob = prob
        self.shortProse = shortProse

    def __str__(self):

        temp = None
        if self.preferredUnit == "F":
            temp = self.tempF
        else:
            temp = self.tempC

        degree_sym = "\u00B0"

        s = f"""
{self.date}, {self.time}:
Temperature:      {temp:.1f}{degree_sym}{self.preferredUnit}
Precipitation %:  {self.prob}%
Windspeed:        {self.windSpeed} {self.windDirection}"""

        return s


class Forecast():

    def __init__(self, location, json, preferredUnit):
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

            obj = Slice(startDate, startTime, temp, tempUnit, self.preferredUnit, windSpeed, windDirection, prob, shortProse)

            self.time_slices.append(obj)

   