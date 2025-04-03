import requests
from config import Config

BASE_URL = 'http://api.openweathermap.org/data/2.5/'

def get_weather(city_id):
    """Fetch current weather data for a given city ID"""
    response = requests.get(f'{BASE_URL}weather', params={
        'id': city_id,
        'appid': Config.OPENWEATHERMAP_API_KEY,
        'units': 'metric'
    })

    if response.status_code == 404:
        return {'error': 'City not found'}, 404
    if response.status_code != 200:
        return {'error': 'Failed to retrieve data from OpenWeatherMap API'}, response.status_code

    data = response.json()
    return {
        'city_id': data['id'],
        'city_name': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description']
    }

def get_forecast(city_id):
    """Fetch 5-day weather forecast data for a given city ID"""
    response = requests.get(f'{BASE_URL}forecast', params={
        'id': city_id,
        'appid': Config.OPENWEATHERMAP_API_KEY,
        'units': 'metric'
    })

    if response.status_code == 404:
        return {'error': 'City not found'}, 404
    if response.status_code != 200:
        return {'error': 'Failed to retrieve data from OpenWeatherMap API'}, response.status_code

    data = response.json()
    forecast_list = []
    seen_dates = set()
    for entry in data['list']:
        datetime_str = entry['dt_txt']
        date_str, time_str = datetime_str.split()
        if time_str == '18:00:00' and date_str not in seen_dates:
            forecast_list.append({
                'date': date_str,
                'temperature': entry['main']['temp'],
                'description': entry['weather'][0]['description']
            })
            seen_dates.add(date_str)
    return {
        'city_id': data['city']['id'],
        'city_name': data['city']['name'],
        'forecast': forecast_list
    }