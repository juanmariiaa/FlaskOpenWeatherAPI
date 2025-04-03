from flask import Flask
from flask_smorest import Api
from config import Config
from api.weather import blp as WeatherBlueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    api = Api(app)
    api.register_blueprint(WeatherBlueprint)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)