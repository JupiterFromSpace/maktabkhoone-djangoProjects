from celery import shared_task
from .models import Task
import requests
from django.core.cache import cache
from django.conf import settings


@shared_task
def delete_done_tasks():
    deleted_count, _ = Task.objects.filter(is_done=True).delete()
    return f'{deleted_count} تسک انجام شده حذف شد.'



@shared_task
def fetch_weather():
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={settings.OPENWEATHER_CITY}"
        f"&appid={settings.OPENWEATHER_API_KEY}"
        f"&units=metric"
        f"&lang=fa"
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = {
            'city': data['name'],
            'temp': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
        }
        cache.set('weather_data', weather, timeout=60 * 20)
        return weather
    return None