from flask_smorest import Blueprint
from schemas.weather import WeatherSchema, HistoricalWeatherSchema, ForecastSchema
from service.openweathermap import get_weather, get_forecast

blp = Blueprint('weather', __name__, url_prefix='/weather', description='Weather API')

@blp.route('/city/<int:city_id>', methods=['GET'])
@blp.response(200, WeatherSchema)
def get_weather_city(city_id):
    """Get current weather for a city by city_id"""
    weather_data = get_weather(city_id)
    return weather_data

@blp.route('/cities', methods=['GET'])
@blp.arguments(HistoricalWeatherSchema, location='query')
@blp.response(200, WeatherSchema(many=True))
def get_weather_cities(args):
    """Get current weather for multiple cities by comma-separated city_ids"""
    city_ids = args['city_ids']
    return [get_weather(city_id) for city_id in city_ids.split(',')]

@blp.route('/forecast/<int:city_id>', methods=['GET'])
@blp.response(200, ForecastSchema)
def get_forecast_city(city_id):
    """Get 5-day forecast for a city by city_id"""
    forecast_data = get_forecast(city_id)
    return forecast_data

@blp.route('/forecast', methods=['GET'])
@blp.arguments(HistoricalWeatherSchema, location='query')
@blp.response(200, ForecastSchema(many=True))
def get_forecast_cities(args):
    """Get 5-day forecast for multiple cities by comma-separated city_ids"""
    city_ids = args['city_ids']
    return [get_forecast(city_id) for city_id in city_ids.split(',')]