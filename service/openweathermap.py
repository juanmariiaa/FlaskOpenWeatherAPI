import requests
from config import Config
from datetime import datetime

BASE_URL = 'http://api.openweathermap.org/data/2.5/'

def get_weather(city_id):
    """
    Fetch current weather data for a given city ID from the OpenWeatherMap API.

    Parameters:
        city_id (int): The OpenWeatherMap city ID.

    Returns:
        dict: Weather information including city ID, name, temperature, description, and timestamp.
              If an error occurs, returns a dictionary with an error message and HTTP status code.
    """
    response = requests.get(f'{BASE_URL}weather', params={
        'id': city_id,
        'appid': Config.OPENWEATHERMAP_API_KEY,
        'units': 'metric'  # Return temperature in Celsius
    })

    # Handle possible errors from the API
    if response.status_code == 404:
        return {'error': 'City not found'}, 404
    if response.status_code != 200:
        return {'error': 'Failed to retrieve data from OpenWeatherMap API'}, response.status_code

    data = response.json()
    dt_unix = data['dt']  # Unix timestamp of the weather data
    dt_str = datetime.utcfromtimestamp(dt_unix).strftime('%Y-%m-%d %H:%M:%S')  # Convert to readable format

    # Return relevant weather information
    return {
        'city_id': data['id'],
        'city_name': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'timestamp': dt_str
    }

def get_forecast(city_id):
    """
    Fetch 5-day weather forecast data for a given city ID, specifically selecting one forecast per day at 18:00:00.

    Parameters:
        city_id (int): The OpenWeatherMap city ID.

    Returns:
        dict: Forecast data including city ID, name, and a list of daily forecasts.
              If an error occurs, returns a dictionary with an error message and HTTP status code.
    """
    response = requests.get(f'{BASE_URL}forecast', params={
        'id': city_id,
        'appid': Config.OPENWEATHERMAP_API_KEY,
        'units': 'metric'  # Return temperature in Celsius
    })

    # Handle possible errors from the API
    if response.status_code == 404:
        return {'error': 'City not found'}, 404
    if response.status_code != 200:
        return {'error': 'Failed to retrieve data from OpenWeatherMap API'}, response.status_code

    data = response.json()
    forecast_list = []
    seen_dates = set()

    # Loop through the list of forecast entries (every 3 hours)
    for entry in data['list']:
        datetime_str = entry['dt_txt']  # Example: "2025-04-07 18:00:00"
        date_str, time_str = datetime_str.split()

        # Only select forecasts at 18:00:00 and avoid duplicate dates
        if time_str == '18:00:00' and date_str not in seen_dates:
            forecast_list.append({
                'date': date_str,
                'temperature': entry['main']['temp'],
                'description': entry['weather'][0]['description']
            })
            seen_dates.add(date_str)

    # Return forecast for selected days
    return {
        'city_id': data['city']['id'],
        'city_name': data['city']['name'],
        'forecast': forecast_list
    }
