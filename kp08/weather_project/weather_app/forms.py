from django import forms
from datetime import date


class WeatherGeneratorForm(forms.Form):
    min_temp = forms.FloatField(initial=10.0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_temp = forms.FloatField(initial=30.0, widget=forms.NumberInput(attrs={'class': 'form-control'}))