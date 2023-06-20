from django import forms

class DownloadComplaintsForm(forms.Form):
    DAY_CHOICES = [
        (1, 'Maandag'),
        (2, 'Dinsdag'),
        (4, 'Donderdag'),
        (5, 'Vrijdag'),
    ]
    AREA_CHOICES = [
        ('CA', 'CA'),
        ('CB', 'CB'),
        ('ZA', 'ZA'),
        ('ZB', 'ZB'),
    ]

    day_of_week = forms.ChoiceField(choices=DAY_CHOICES, label='Day of Week', required=False)
    area = forms.ChoiceField(choices=AREA_CHOICES, label='Area', required=False)
