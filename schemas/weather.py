from marshmallow import Schema, fields

class WeatherSchema(Schema):
    city_id = fields.Int(required=True)
    city_name = fields.Str(required=True)
    temperature = fields.Float(required=True)
    description = fields.Str(required=True)

class HistoricalWeatherSchema(Schema):
    city_ids = fields.Str(required=True)

class ForecastEntrySchema(Schema):
    date = fields.Str(required=True)
    temperature = fields.Float(required=True)
    description = fields.Str(required=True)

class ForecastSchema(Schema):
    city_id = fields.Int(required=True)
    city_name = fields.Str(required=True)
    forecast = fields.List(fields.Nested(ForecastEntrySchema), required=True)

