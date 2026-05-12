from django import forms
from datetime import date, timedelta


class WeatherGeneratorForm(forms.Form):
    min_temp = forms.FloatField(initial=10.0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_temp = forms.FloatField(initial=30.0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    first_date = forms.DateField(initial=date.today(), widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    last_date = forms.DateField(initial=date.today() + timedelta(days=5), widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    min_pressure = forms.FloatField(initial=700.0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_pressure = forms.FloatField(initial=900.0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    min_humidity = forms.FloatField(initial=40.0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_humidity = forms.FloatField(initial=80.0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    min_speed = forms.FloatField(initial=0.0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_speed = forms.FloatField(initial=20.0, widget=forms.NumberInput(attrs={'class': 'form-control'}))