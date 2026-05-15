from django.shortcuts import render
import random
import pandas as pd
import plotly.express as px
from .models import WeatherData
from datetime import date, timedelta
from django.http import JsonResponse

def update_db():
    WeatherData.objects.all().delete()
    start_date = date.today()
    for i in range(10):
        WeatherData.objects.create(
            date=start_date + timedelta(days=i),
            temperature=round(random.uniform(-10, 35), 1),
            pressure=round(random.uniform(980, 1050), 1),
            humidity=round(random.uniform(20, 100), 1),
            speed=round(random.uniform(0, 20), 1)
        )


def weather_dashboard(request):
    if request.method == "POST":
        print(f'if post:request:{request}')
        update_db()
        new_data = list(WeatherData.objects.all().values().order_by('date'))
        return JsonResponse({'status': 'success', 'data': new_data})
    
    print(f'request:{request}')
    update_db()
    data = WeatherData.objects.all().order_by('date')
    df = pd.DataFrame(list(data.values()))

    temp_plot = ""
    press_plot = ""
    hum_plot = ""
    speed_plot = ""
    if not df.empty:
        fig_temp = px.line(df, x='date', y='temperature', title='Temperature Trend, °C', markers=True)
        temp_plot = fig_temp.to_html(full_html=False, div_id='temp_plot')
        fig_press = px.bar(df, x='date', y='pressure', title='Pressure Trend, mmHg')
        press_plot = fig_press.to_html(full_html=False, div_id='press_plot')
        fig_hum = px.line(df, x='date', y='humidity', title='Humidity Trend, %', markers=True)
        hum_plot = fig_hum.to_html(full_html=False, div_id='hum_plot')
        fig_speed = px.line(df, x='date', y='speed', title='Wind Speed Trend, m/s', markers=True)
        speed_plot = fig_speed.to_html(full_html=False, div_id='speed_plot')

    return render(request, 'dashboard.html', {
        'data': data,
        'temp_plot': temp_plot,
        'press_plot': press_plot,
        'hum_plot': hum_plot,
        'speed_plot': speed_plot,}  
    )