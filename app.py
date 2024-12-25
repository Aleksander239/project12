import requests
from flask import Flask, render_template, request, jsonify
from API import get_weather
from check_weather import check_bad_weather

api_key = 'zNElxvS2svZAuiMKUpfO0v89LCSv7okB'

app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_city = request.form['start_city']
        end_city = request.form['end_city']

        # Получаем координаты начальной точки
        start_location_url = f'http://dataservice.accuweather.com/locations/v1/cities/search?q={start_city}&apikey={api_key}'
        start_location_response = requests.get(start_location_url)
        start_location_data = start_location_response.json()

        if len(start_location_data) > 0:
            start_lat = start_location_data[0]['GeoPosition']['Latitude']
            start_lon = start_location_data[0]['GeoPosition']['Longitude']
        else:
            return render_template('index.html', error="Не удалось найти начальный город.")

        # Получаем координаты конечной точки
        end_location_url = f'http://dataservice.accuweather.com/locations/v1/cities/search?q={end_city}&apikey={api_key}'
        end_location_response = requests.get(end_location_url)
        end_location_data = end_location_response.json()

        if len(end_location_data) > 0:
            end_lat = end_location_data[0]['GeoPosition']['Latitude']
            end_lon = end_location_data[0]['GeoPosition']['Longitude']
        else:
            return render_template('index.html', error="Не удалось найти конечный город.")

        # Получаем погодные данные для начальной точки
        start_weather = get_weather(start_lat, start_lon)
        if 'error' in start_weather:
            return render_template('index.html', error="Не удалось получить данные о погоде для начального города.")

        # Получаем погодные данные для конечной точки
        end_weather = get_weather(end_lat, end_lon)
        if 'error' in end_weather:
            return render_template('index.html', error="Не удалось получить данные о погоде для конечного города.")

        # Проверяем качество погоды
        if check_bad_weather(start_weather):
            start_weather_condition = 'Погода - супер!'
        else:
            start_weather_condition = 'Ой-ой, погода плохая'

        if check_bad_weather(end_weather):
            end_weather_condition = 'Погода - супер!'
        else:
            end_weather_condition = 'Ой-ой, погода плохая'

        return render_template('result.html', start_city=start_city, end_city=end_city,
                               start_weather_condition=start_weather_condition,
                               end_weather_condition=end_weather_condition)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)