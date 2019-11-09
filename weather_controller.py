from weather_model import Weather
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import requests, os

KEY = os.environ['DARK_SKY_KEY'].strip('[]')
options = "exclude=currently,minutely,hourly,alerts&amp;units=si"

class WController:

	def get_location(self, location):
		return Nominatim().geocode(location, language='en_US')

	def get_reports(self, data, location):
		d_from = datetime.strptime(data['date_from'], '%Y-%m-%d')
		d_to = datetime.strptime(data['date_to'], '%Y-%m-%d')

		delta = d_to - d_from

		lat = str(location.latitude)
		long = str(location.longitude)

		reports = []

		for i in range(delta.days+1):
			date = (d_from + timedelta(days=i)).strftime('%Y-%m-%d')
			search = date+"T00:00:00"
			response = requests.get("https://api.darksky.net/forecast/"+str(KEY)+"/"+lat+","+long+","+search+"?"+options).json()
			print("RESPONSE:", response)
			print("KEY: ", repr(KEY))
			report_date = (d_from + timedelta(days=i)).strftime('%Y-%m-%d %A')
			unit = ' F' if response['flags']['units'] == 'us' else ' C'

			min = str(response['daily']['data'][0]['apparentTemperatureMin'])+unit
			max = str(response['daily']['data'][0]['apparentTemperatureMax'])+unit
			summary = response['daily']['data'][0]['summary']
			icon = response['daily']['data'][0]['icon']
			precipitation = None
			probability = None
			chance  = None
			if 'precipProbability' in response['daily']['data'][0] and 'precipType' in response['daily']['data'][0]:
				precipitation = response['daily']['data'][0]['precipType']
				probability = response['daily']['data'][0]['precipProbability']
			if (precipitation == 'rain' and probability != None):
				chance = "chance of rain: %.2f%%" % (probability*100)

			report = Weather(report_date, max, min, summary, chance, icon)
			reports.append(report)

		return reports
