from django.shortcuts import render
import random
import pandas as pd
import plotly.express as px
from django.shortcuts import render, redirect
from .models import WeatherData
from datetime import date, timedelta
from .forms import WeatherGeneratorForm

form=None

def weather_dashboard(request):
    if request.method == "POST":
        global form
        form = WeatherGeneratorForm(request.POST or None)
        if form.is_valid():
            t_min, t_max = form.cleaned_data['min_temp'], form.cleaned_data['max_temp']

        WeatherData.objects.all().delete()  
        start_date = date.today()
        count = 10
        for i in range(count):
            WeatherData.objects.create(
                date=start_date + timedelta(days=i),
                temperature=round(random.uniform(t_min, t_max),1),  # Випадкова температура
                pressure=round(random.uniform(700, 900),1),    # Випадковий тиск
                humidity=round(random.uniform(40, 80),1),      # Випадкова вологість
                speed=round(random.uniform(0, 20),1)           # Випадкова швидкість вітру
            )
        return redirect('dashboard')
    
    data = WeatherData.objects.all().order_by('date')
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
    else:
        form = WeatherGeneratorForm()

    return render(request, 'dashboard.html', {'data': data, 'temp_plot': temp_plot, 'press_plot': press_plot, 'hum_plot': hum_plot, 'speed_plot': speed_plot, 'form': form})