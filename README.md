# 🌦️ Flask Weather API Proxy

This project is a small Flask application that acts as a proxy to the [OpenWeatherMap API](https://openweathermap.org/api). It exposes several endpoints to retrieve current and historical weather information for one or more cities. It also includes a persistence layer with SQLAlchemy and PostgreSQL to cache the data for performance and historical access.

---

## 📌 Features

- Get current weather by city ID
- Get current weather for multiple cities by comma-separated city IDs
- Get historical weather data (last 5 days) for multiple cities
- Caches data using PostgreSQL to avoid repeated external API calls
- Automatically retrieves and stores data if not available in the database
- Utilizes Marshmallow for data serialization/deserialization
- Clean architecture with Flask-Smorest for API structure

---

## 📦 Technologies Used

- Python 3
- Flask
- Flask-Smorest
- SQLAlchemy
- Marshmallow
- PostgreSQL
- OpenWeatherMap API

---

## 🚀 API Endpoints

### `GET /weather/<city_id>`
Retrieve the current weather data for a single city by its `city_id`.

### `GET /weather/cities?city_ids=ID1,ID2,...`
Retrieve the current weather data for multiple cities using a comma-separated list of `city_ids`.

### `GET /forecast/<city_id>`
Retrieve the historical weather data (up to 5 days back) for a single city by its `city_id`.

### `GET /weather/forecast?city_ids=ID1,ID2,...`
Retrieve the historical weather data (up to 5 days back) for multiple cities using a comma-separated list of `city_ids`.

---

### 🔗 Relationships
- One-to-many relationship between `City` and `WeatherInformation`
- Cascading deletes: when a city is removed, its weather data is also deleted

---

## 🧪 Marshmallow Schemas

Marshmallow is used for request/response validation and serialization.
