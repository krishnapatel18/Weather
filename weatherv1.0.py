import requests

class WeatherDietAdvisor:
    def __init__(self, weather_api_key, weather_api_url, open_weather_map_city_id):
        self.weather_api_key = weather_api_key
        self.weather_api_url = weather_api_url
        self.city_id = open_weather_map_city_id

    def get_current_temperature(self):
        url = f"{self.weather_api_url}?id={self.city_id}&appid={self.weather_api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data.get('main'): 
                return data.get('main', {}).get('temp') - 273.15
            else:
                print("Error: 'main' key not found in weather data")
                return None  
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            return None  

    def suggest_diet(self):
        temperature = self.get_current_temperature()
        suggestion = ""

        if temperature is not None:  
            if temperature > 35:  
                suggestion = "It's hot outside! Consider hydrating with refreshing drinks like lassi, coconut water, or buttermilk."
            elif temperature < 20:  
                suggestion = "Feeling chilly? Warm yourself up with a cup of hot chocolate, ginger tea, or a bowl of warm soup."
            else:
                suggestion = "Enjoy the pleasant weather! You have a variety of dietary options today."
        else:
            suggestion = "Unable to determine weather conditions. Please try again later."

        return suggestion

weather_api_key = "<use your api key here>"
weather_api_url = "https://api.openweathermap.org/data/2.5/weather"
city_id = 2988507           

advisor = WeatherDietAdvisor(weather_api_key, weather_api_url, city_id)
temperature = advisor.get_current_temperature()
suggestion = advisor.suggest_diet()
print(temperature, suggestion)
