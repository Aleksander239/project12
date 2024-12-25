import requests

api_key = 'zNElxvS2svZAuiMKUpfO0v89LCSv7okB'

# Координаты города
lat = 51.7558
lon = 3.6173



def get_weather(lat, lon):
    # Сначала получаем location key по координатам
    location_url = f'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={api_key}&q={lat},{lon}'
    location_response = requests.get(location_url)
    location_data = location_response.json()

    if 'Key' in location_data:
        location_key = location_data['Key']

        # Затем используем location key для получения данных о погоде
        weather_url = f'http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}&details=true'
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        if len(weather_data) > 0:
            weather_info = {
                'temperature': weather_data[0]['Temperature']['Metric']['Value'],
                'humidity': weather_data[0]['RelativeHumidity'],
                'wind_speed': weather_data[0]['Wind']['Speed']['Metric']['Value'],
                'precipitation': weather_data[0]['Precip1hr']['Metric']['Value']
            }

            return weather_info
        else:
            return {'error': 'No weather data available for this location.'}
    else:
        return {'error': 'Location not found.'}

