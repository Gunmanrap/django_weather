from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm


def index(request):
    appid = ''
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
    form = CityForm
    cities = City.objects.all()
    all_cities = []
    for city in cities:
        data = requests.get(url.format(city.name)).json()
        # Инструкция которая удаляет несуществующие города из базы чтобы не вызывать ошибку 404
        if data['cod'] == '404':
            cities.get(name=city).delete()
        else:
            city_info = {
                'city': city.name,
                'temp': data['main']['temp'],
                'icon': data['weather'][0]['icon'],
                'cod': data['cod'],
                'id': cities.filter(name=city.name).values().get(name=city.name)['id']
                }
            all_cities.append(city_info)
            # Следующий цикл удаляет запись из блока информации, но не удаляет из базы данных, также удаляет дубликаты городов на одном языке
            for n in all_cities:
                if n in all_cities and all_cities.count(n) > 1:
                    all_cities.remove(n)
            # Следующая инструкция проверяет наличие дубликатов в базе данных и удаляет их, но не удаляет дубликаты на разных языках.
            if city_info['city'] == city.name and cities.filter(name=city).count() > 1:
                cities.get(id=city.id).delete()
    context = {'all_info': all_cities, 'form': form}
    return render(request, 'weather_app/index.html', context)

# Функция для кнопки удаления города из блока информации, также удаляет из базы.
def delete(request, id):
    city = City.objects.get(id=id)
    city.delete()
    return HttpResponseRedirect("/")
