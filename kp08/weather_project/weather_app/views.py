from django.shortcuts import render, redirect
import random
import pandas as pd
import plotly.express as px
from .models import WeatherData
from datetime import date, timedelta
from .forms import WeatherGeneratorForm

def weather_dashboard(request):
    if request.method == "POST":
        form = WeatherGeneratorForm(request.POST)
        if form.is_valid():
            t_min = form.cleaned_data['min_temp']
            t_max = form.cleaned_data['max_temp']
            p_min = form.cleaned_data['min_pressure']
            p_max = form.cleaned_data['max_pressure']
            h_min = form.cleaned_data['min_humidity']
            h_max = form.cleaned_data['max_humidity']
            s_min = form.cleaned_data['min_speed']
            s_max = form.cleaned_data['max_speed']
            first_date = form.cleaned_data['first_date']
            last_date = form.cleaned_data['last_date']

            WeatherData.objects.all().delete()
            start_date = first_date
            count = 10
            for i in range(count):
                WeatherData.objects.create(
                    date=start_date + timedelta(days=i),
                    temperature=round(random.uniform(t_min, t_max), 1),
                    pressure=round(random.uniform(p_min, p_max), 1),
                    humidity=round(random.uniform(h_min, h_max), 1),
                    speed=round(random.uniform(s_min, s_max), 1)
                )
        return redirect('dashboard')
    else:
        # Для GET-запиту створюємо НОВУ незв'язану форму з initial значеннями
        form = WeatherGeneratorForm()

    data = WeatherData.objects.all().order_by('date')
    df = pd.DataFrame(list(data.values()))

    temp_plot = ""
    press_plot = ""
    hum_plot = ""
    speed_plot = ""
    if not df.empty:
        fig_temp = px.line(df, x='date', y='temperature', title='Temperature Trend, °C', markers=True)
        temp_plot = fig_temp.to_html(full_html=False)
        fig_press = px.bar(df, x='date', y='pressure', title='Pressure Trend, mmHg')
        press_plot = fig_press.to_html(full_html=False)
        fig_hum = px.line(df, x='date', y='humidity', title='Humidity Trend, %', markers=True)
        hum_plot = fig_hum.to_html(full_html=False)
        fig_speed = px.line(df, x='date', y='speed', title='Wind Speed Trend, m/s', markers=True)
        speed_plot = fig_speed.to_html(full_html=False)

    return render(request, 'dashboard.html', {
        'data': data,
        'temp_plot': temp_plot,
        'press_plot': press_plot,
        'hum_plot': hum_plot,
        'speed_plot': speed_plot,
        'form': form,
    })