from django import forms

class RouteSearchForm(forms.Form):
    route_id = forms.CharField(required=True, label='Route ID', widget=forms.TextInput(attrs={'placeholder': 'Enter Route ID'}))
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

class FractionSearchForm(forms.Form):
    fraction = forms.CharField(required=True, label='Fraction', widget=forms.TextInput(attrs={'placeholder': 'Enter Fraction ID'}))
    area = forms.ChoiceField(choices=[('', '---'), ('stedelijk', 'stedelijk'), ('landelijk', 'landelijk')],
                             required=False)
    day_of_week = forms.ChoiceField(choices=[('', '---'), ('1', 'maandag'), ('2', 'dinsdag'), ('4', 'donderdag'), ('5', 'vrijdag')],
                             required=False)
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
