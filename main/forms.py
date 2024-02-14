from django import forms


class UpdatePosition(forms.Form):
    position = forms.IntegerField(min_value=0, widget=forms.HiddenInput())
    is_finished = forms.BooleanField(widget=forms.HiddenInput(), required=False)
