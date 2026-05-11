from django.shortcuts import render
import random
import pandas as pd
import plotly.express as px
from django.shortcuts import render, redirect
from .models import WeatherData
from datetime import date, timedelta

def weather_dashboard(request):
    if request.method == "POST":
        WeatherData.objects.all().delete()  
        start_date = date.today()
        for i in range(10):
            WeatherData.objects.create(
                date=start_date + timedelta(days=i),
                temperature=round(random.uniform(15, 30),1),  # Випадкова температура
                pressure=round(random.uniform(700, 900),1),    # Випадковий тиск
                humidity=round(random.uniform(40, 80),1),      # Випадкова вологість
                speed=round(random.uniform(0, 20),1)           # Випадкова швидкість вітру
            )
        return redirect('dashboard')
    
    data = WeatherData.objects.all()
    df = pd.DataFrame(list(data.values()))

    temp_plot=""
    press_plot=""
    hum_plot=""
    speed_plot=""
    if not df.empty:
        fig_temp = px.line(df, x='date', y='temperature', title='Temperature Trend, °C', markers=True)
        temp_plot = fig_temp.to_html(full_html=False)
        fig_press = px.line(df, x='date', y='pressure', title='Pressure Trend, mmHg', markers=True)
        press_plot = fig_press.to_html(full_html=False)
        fig_hum = px.line(df, x='date', y='humidity', title='Humidity Trend, %', markers=True)
        hum_plot = fig_hum.to_html(full_html=False)
        fig_speed = px.line(df, x='date', y='speed', title='Wind Speed Trend, m/s', markers=True)
        speed_plot = fig_speed.to_html(full_html=False)

    return render(request, 'dashboard.html', {'data': data, 'temp_plot': temp_plot, 'press_plot': press_plot, 'hum_plot': hum_plot, 'speed_plot': speed_plot})