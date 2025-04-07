from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    weather_info = db.relationship('WeatherInformation', back_populates='city', cascade='all, delete-orphan')

class WeatherInformation(db.Model):
    __tablename__ = 'weather_information'

    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.String(50), nullable=False)  # 👈 Como string

    city = db.relationship('City', back_populates='weather_info')

