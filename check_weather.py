weather_dict = {
                'temperature': 15.0,
                'humidity': 85,
                'wind_speed': 1,
                'precipitation': 11
}
def check_bad_weather(weather_dict):
    if (weather_dict['temperature'] > 35) or (weather_dict['temperature'] < -15):
        return False
    elif weather_dict['wind_speed'] > 15.2:
        return False
    elif weather_dict['precipitation'] > 15:
        return False
    else:
        return True

print(check_bad_weather(weather_dict))