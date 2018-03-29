#!/usr/bin/python


from check_weather import current_hour
from check_weather import process_info


weather_url = 'http://www.weather.com.cn/weather1d/101020100.shtml#search'

print current_hour()

process_info(weather_url)