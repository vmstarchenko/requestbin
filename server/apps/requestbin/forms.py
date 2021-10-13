from django import forms


class RequestForm(forms.Form):
    _sleep = forms.FloatField(required=False)
    _status_code = forms.IntegerField(required=False)
