from flask_smorest import Blueprint
from schemas.weather import WeatherSchema, HistoricalWeatherSchema, ForecastSchema
from service.openweathermap import get_weather, get_forecast
from model.models import db, City, WeatherInformation

# Define the Blueprint for weather-related routes
blp = Blueprint('weather', __name__, url_prefix='/weather', description='Weather API')

@blp.route('/city/<int:city_id>', methods=['GET'])
@blp.response(200, WeatherSchema)
def get_weather_city(city_id):
    """
    Retrieve current weather data for a specific city by its city ID.

    Args:
        city_id (int): The OpenWeatherMap city ID.

    Returns:
        dict: A dictionary with weather data including temperature, description, and timestamp.
              If the city is not found, returns an error message.
    """
    city = City.query.get(city_id)

    # Call external API to get current weather
    weather_data = get_weather(city_id)

    # Return error if API fails
    if 'error' in weather_data:
        return {'error': 'Weather data not found'}, 404

    # If the city doesn't exist in the DB, create it
    if not city:
        city = City(id=city_id, name=weather_data['city_name'])
        db.session.add(city)
        db.session.flush()  # Ensures city.id is available

    # Update weather info if it already exists
    if city.weather_info:
        weather_info = city.weather_info[0]
        weather_info.temperature = weather_data['temperature']
        weather_info.description = weather_data['description']
        weather_info.timestamp = weather_data['timestamp']
    else:
        # Create new weather info entry
        weather_info = WeatherInformation(
            city_id=city.id,
            temperature=weather_data['temperature'],
            description=weather_data['description'],
            timestamp=weather_data['timestamp']
        )
        city.weather_info.append(weather_info)

    db.session.commit()

    return {
        'city_id': city.id,
        'city_name': city.name,
        'temperature': weather_info.temperature,
        'description': weather_info.description,
        'timestamp': weather_info.timestamp
    }

@blp.route('/cities', methods=['GET'])
@blp.arguments(HistoricalWeatherSchema, location='query')
@blp.response(200, WeatherSchema(many=True))
def get_weather_cities(args):
    """
    Retrieve current weather data for multiple cities based on comma-separated city IDs.

    Query Parameters:
        city_ids (str): Comma-separated list of OpenWeatherMap city IDs.

    Returns:
        list: A list of dictionaries, each containing weather data for a city.
    """
    city_ids = args['city_ids']
    weather_data_list = []

    for city_id in city_ids.split(','):
        city_id = int(city_id.strip())
        city = City.query.get(city_id)

        # Call external API
        weather_data = get_weather(city_id)

        if 'error' in weather_data:
            continue  # Skip invalid city IDs

        # Create the city if it doesn't exist
        if not city:
            city = City(id=city_id, name=weather_data['city_name'])
            db.session.add(city)
            db.session.flush()

        # Update or insert weather information
        if city.weather_info:
            weather_info = city.weather_info[0]
            weather_info.temperature = weather_data['temperature']
            weather_info.description = weather_data['description']
            weather_info.timestamp = weather_data['timestamp']
        else:
            weather_info = WeatherInformation(
                city_id=city.id,
                temperature=weather_data['temperature'],
                description=weather_data['description'],
                timestamp=weather_data['timestamp']
            )
            city.weather_info.append(weather_info)

        db.session.commit()

        weather_data_list.append({
            'city_id': city.id,
            'city_name': city.name,
            'temperature': weather_info.temperature,
            'description': weather_info.description,
            'timestamp': weather_info.timestamp
        })

    return weather_data_list

@blp.route('/forecast/<int:city_id>', methods=['GET'])
@blp.response(200, ForecastSchema)
def get_forecast_city(city_id):
    """
    Retrieve 5-day forecast data for a specific city.

    Args:
        city_id (int): The OpenWeatherMap city ID.

    Returns:
        dict: A dictionary with forecast data (one entry per day at 18:00:00).
    """
    forecast_data = get_forecast(city_id)
    return forecast_data

@blp.route('/forecast', methods=['GET'])
@blp.arguments(HistoricalWeatherSchema, location='query')
@blp.response(200, ForecastSchema(many=True))
def get_forecast_cities(args):
    """
    Retrieve 5-day forecast data for multiple cities.

    Query Parameters:
        city_ids (str): Comma-separated list of OpenWeatherMap city IDs.

    Returns:
        list: A list of forecast data dictionaries (one per city).
    """
    city_ids = args['city_ids']
    return [get_forecast(int(city_id.strip())) for city_id in city_ids.split(',')]
