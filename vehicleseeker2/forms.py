# forms.py
from django import forms

class VehicleSearchForm(forms.Form):
    vehicle_query = forms.CharField(label='Search Vehicle', max_length=100)
