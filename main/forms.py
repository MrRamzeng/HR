from django import forms


class UpdatePosition(forms.Form):
    position = forms.IntegerField(min_value=0) #, widget=forms.HiddenInput())
