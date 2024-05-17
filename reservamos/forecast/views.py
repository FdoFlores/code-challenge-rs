from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

# Create your views here.
class ForecastView(APIView):
    # This is a very simple view
    # this view takes the sent param from the URL and makes a request to the reservamos API to get every the list of cities and coordinates that match the sent string
    # I filter the result to only get the cities from the result
    # then I go trough every city and look for the weather of those coordinates
    # then I just save that info into a dictionary that I return to the endpoint

    # returns cities when found cities
    # returns error when a api call fails
    # returns not found when the api call returned no cities
    
    def get(self, request, city):
        cities = {}
        url = f'https://search.reservamos.mx/api/v2/places?q={city}'
        headers = {'User-Agent': 'reservamos'}
        response = requests.get(url, headers=headers)

        filtered = None
        if response.status_code == 201:
            data = response.json()
            required_type = 'city'

            # Filter cities in the items of the response.
            filtered = list(filter(lambda item: item.get('result_type') == required_type, data))
            # Now we only have the cities in 'filtered'
        else:
            return Response({'message: Could not fetch the response from reservamos API (Just try again it fails randomly).'}, status=status.HTTP_400_BAD_REQUEST)

        if not filtered:
            return Response({'message: No cities found.'}, status=status.HTTP_404_NOT_FOUND)

        for city in filtered:
            lat = city['lat']
            lon = city['long']
            owk = 'a5a47c18197737e8eeca634cd6acb581' # Saving this variable in a .ENV would be better.
            weather_url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={owk}&units=metric'
            weather_headers = {
                'User-Agent': 'reservamos'
            }
            weather_req = requests.get(weather_url, weather_headers)
            if weather_req.status_code == 200:
                weather_data = weather_req.json()
                city_name = city['city_name']
                # if the actual city is not in the cities dictionary
                # we iterate the days of the weather and add them to the response dict list.
                if city_name not in cities:
                    cities[city_name] = []
                    for day in weather_data['daily']:
                        cities[city_name].append({
                            'min': day['temp']['min'],
                            'max': day['temp']['max']
                        })
            else:
                return Response({'message: Could not fetch the response from OpenWeather API.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(cities, status=status.HTTP_200_OK)