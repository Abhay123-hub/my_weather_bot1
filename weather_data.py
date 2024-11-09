from app_logger import logger
from app_exception.exception import AppException
import pyowm
import sys

class WeatherData:
    def __init__(self):
        self.owmapikey = "973ea382262d69b935b4ba03cd78bf60"
        self.owm = pyowm.OWM(self.owmapikey)
    
    def process_request(self, req):
        try:
            self.result = req.get("queryResult")
            self.parameters = self.result.get("parameters")
            self.city = self.parameters.get("city_name")
            self.observation = self.owm.weather_at_place(str(self.city))
            w = self.observation.get_weather()
            self.latlon_res = self.observation.get_location()

            self.lat = str(self.latlon_res.get_lat())  # Latitude
            self.lon = str(self.latlon_res.get_lon())  # Longitude

            self.wind_result = w.get_wind()
            self.wind_speed = str(self.wind_result.get('speed'))
            self.humidity = str(w.get_humidity())

            # Corrected 'celsius' spelling and variable names
            self.celsius_result = w.get_temperature('celsius')
            self.temp_min_celsius = str(self.celsius_result.get('temp_min'))
            self.temp_max_celsius = str(self.celsius_result.get("temp_max"))

            # Updated speech text to reference corrected variables
            speech = (
                f"Today's the weather in {self.city}: Humidity: {self.humidity}, "
                f"Wind Speed: {self.wind_speed}, Minimum Temperature: {self.temp_min_celsius}°C, "
                f"Maximum Temperature: {self.temp_max_celsius}°C"
            )
        except Exception as e:
            raise AppException(e, sys) from e 

        return {
            "fullfillmentText": speech,
            "displayText": speech
        }
