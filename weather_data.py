# Importing required packages
from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests
import os
from datetime import datetime
import secrets

app = Flask(__name__, template_folder='templates')
app.secret_key = secrets.token_hex(16)

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather_info(self, location):
        # Construct API request link
        complete_api_link = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}"
        
        # Fetch weather data from API
        api_link = requests.get(complete_api_link)
        api_data = api_link.json()

        # Process API response
        if api_data['cod'] == 404:
            return {"error": f"Invalid city: {location}, Please check your city name"}
        else:
            # Extract relevant weather information from API response
            temp_city = ((api_data['main']['temp']) - 273.15)
            temp_feels_like = ((api_data['main']['feels_like']) - 273.15)
            temp_min = ((api_data['main']['temp_min']) - 273.15)
            temp_max = ((api_data['main']['temp_max']) - 273.15)
            pressure = api_data['main']['pressure']
            weather_desc = api_data['weather'][0]['description']
            hmdt = api_data['main']['humidity']
            wind_spd = api_data['wind']['speed']
            date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")
            visibility = api_data["visibility"]
            country = api_data['sys']['country']

            # Package weather information into a dictionary
            weather_info = {
                "location": location.upper(),
                "country": country,
                "date_time": date_time,
                "current_temperature": round(temp_city, 2),
                "feels_like_temperature": round(temp_feels_like, 2),
                "minimum_temperature": round(temp_min, 2),
                "maximum_temperature": round(temp_max, 2),
                "weather_description": weather_desc,
                "pressure": pressure,
                "humidity": hmdt,
                "wind_speed": wind_spd,
                "visibility": visibility
            }
            return weather_info
    
    def get_historical_and_future_weather(self, location):
        # Placeholder function, replace with actual implementation
        pass

# Route for the login page
@app.route('/')
def login_page():
    return render_template('login.html')

# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    # Here you can implement your login logic
    # For demonstration purposes, let's just print the credentials
    print("Username:", username)
    print("Password:", password)
    
    # Assuming successful login, redirect to the index page
    return redirect(url_for('index'))
        
# Route for the home page
@app.route('/index.html')
def index():
    return render_template('index.html')

# Route to fetch weather data
@app.route('/weather')
def get_weather():
    api_key = os.environ.get('test1_weather_apikey')
    weather_api = WeatherAPI(api_key)
    city = request.args.get('city')
    if city:
        # Fetch weather information for the provided city
        weather_info = weather_api.get_weather_info(city)
        return jsonify(weather_info)
    else:
        # Return an error message if no city is provided
        return jsonify({"error": "Please provide a city name"})
    


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
