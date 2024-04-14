from django.test import TestCase
import requests

class TemperatureAPITest(TestCase):
    def test_temperature_equality(self):
        # Fetch temperature from custom API
        response_custom = requests.post('http://3.75.204.56:8000/api/temperature', json={"city": "Oslo"})
        temp_custom = response_custom.json()['temperature']

        # Fetch temperature from OpenWeatherMap
        response_owm = requests.get('https://api.openweathermap.org/data/2.5/weather?q=Oslo&appid=d2a2b4ae87b93c165c5421cee9970939&units=metric')
        temp_owm = response_owm.json()['main']['temp']

        # Compare temperatures
        self.assertAlmostEqual(temp_custom, temp_owm, places=1, msg="Temperatures do not match")
