from django import forms


class UpdatePosition(forms.Form):
    position = forms.IntegerField(min_value=0, widget=forms.HiddenInput())


class UpdatePagePosition(forms.Form):
    position = forms.IntegerField(min_value=0, widget=forms.HiddenInput())
    has_read = forms.BooleanField(widget=forms.HiddenInput(), required=False)
