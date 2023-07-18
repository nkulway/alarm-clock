import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get('WEATHER_API_KEY')

def weather():
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat=41.40&lon=2.17&appid={api_key}&units=imperial')
    return res.json()