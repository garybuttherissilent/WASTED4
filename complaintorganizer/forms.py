from django import forms


class DownloadComplaintsForm(forms.Form):
    COMPLAINTS_TYPE_CHOICES = [
        ('latest', 'Latest Complaints'),
        ('recurring', 'Recurring Complaints'),
    ]
    FILTER_FIELD_CHOICES = [
        ('route_id', 'Route ID'),
        ('street_name', 'Street Name'),
    ]

    complaints_type = forms.ChoiceField(choices=COMPLAINTS_TYPE_CHOICES)
    filter_field = forms.ChoiceField(choices=FILTER_FIELD_CHOICES)
    filter_value = forms.CharField(max_length=200)
