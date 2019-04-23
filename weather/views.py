import requests
from django.http import HttpResponseRedirect

from django.shortcuts import render,reverse
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=806085ae81a8afc282a4331949e2ae61'


    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('index'))
        
    form = CityForm()


    cities = City.objects.all()


    weather_data = []
    # we use try here because if city name is not found in api database the
    # it will give key error
    try:
        for city in cities:

            r = requests.get(url.format(city)).json()
            
    
            city_weather = {
                'city' : city.name,
                'temperature' : r['main']['temp'],
                'description' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon'],
            }

            weather_data.append(city_weather)
    except KeyError:
        pass
        
    context = {
        'weather_data' : weather_data,
        'form': form,
    }
  
    return render(request, 'weather/weather.html',context)