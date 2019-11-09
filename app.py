from flask import Flask, render_template, request
from flask_cors import CORS
from weather_controller import WController

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
	return render_template('index.html')

@app.route('/weather', methods=['POST','GET'])
def weather():
	if request.method == 'POST':
		data = request.json
		location = data['location']

		weather = WController()

		geo = weather.get_location(location)
		if geo == None:
			address = "unknown location"
			template = render_template('reports.html', weather_address=address)
			return template

		address = geo.address
		reports = weather.get_reports(data, geo)

		template = render_template('reports.html', weather_address = address, weather_reports=reports)
	return template

if __name__ == '__main__':
	app.run(debug=False,host='0.0.0.0')
