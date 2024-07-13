import requests

class WeatherDietAdvisor:
    def __init__(self, weather_api_key, weather_api_url, open_weather_map_city_id, nutrition_api_key, nutrition_api_base_url):
        self.weather_api_key = weather_api_key
        self.weather_api_url = weather_api_url
        self.city_id = open_weather_map_city_id
        self.nutrition_api_key = nutrition_api_key
        self.nutrition_api_base_url = nutrition_api_base_url

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
            temperature_category = self.get_temperature_category(temperature)
            nutrition_suggestions = self.get_nutrition_suggestions(temperature_category)
            suggestion = f"Based on the weather ({temperature:.1f}°C), here are some dietary suggestions:\n"
            for item in nutrition_suggestions:
                suggestion += f"- {item['name']}\n"
        else:
            suggestion = "Unable to determine weather conditions. Please try again later."

        return suggestion

    def get_temperature_category(self, temperature):
        if temperature > 35:
            return "hot"
        elif temperature < 20:
            return "cold"
        else:
            return "moderate"

    def get_nutrition_suggestions(self, temperature_category):
        nutrition_api_url = f"{self.nutrition_api_base_url}?q={temperature_category}&app_id=facecedd&app_key=<use your api key here>"
        # print(nutrition_api_url)
        response = requests.get(nutrition_api_url)

        if response.status_code == 200:
            data = response.json()
            suggestions = []
            for hit in data.get('hits', []):
                suggestions.append({'name': hit['recipe']['label']})
            return suggestions
        else:
            print(f"Error: Nutrition API request failed with status code {response.status_code}")
            return []  

weather_api_key = "<use your api key here>"
weather_api_url = "https://api.openweathermap.org/data/2.5/weather"
city_id = 2988507
nutrition_api_key = "<use your api key here>"  
nutrition_api_base_url = "https://api.edamam.com/search"  

advisor = WeatherDietAdvisor(weather_api_key, weather_api_url, city_id, nutrition_api_key, nutrition_api_base_url)
suggestion = advisor.suggest_diet()
print(suggestion)
