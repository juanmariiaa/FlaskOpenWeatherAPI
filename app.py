from flask import Flask
from flask_smorest import Api
from flask_cors import CORS  # Add this import
from config import Config
from api.weather import blp as WeatherBlueprint
from model.models import db


def create_app():
    app = Flask(__name__)
    # Enable CORS for your Flask app
    CORS(app)  # Add this line

    app.config.from_object(Config)
    db.init_app(app)
    api = Api(app)
    api.register_blueprint(WeatherBlueprint)
    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)