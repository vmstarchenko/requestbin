from django import forms


class RequestForm(forms.Form):
    _sleep = forms.FloatField(required=False)
    _encoding = forms.CharField(required=False)
    _status_code = forms.IntegerField(required=False)
    _content_type = forms.CharField(required=False)
