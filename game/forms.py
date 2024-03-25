from django import forms


class GameForm(forms.Form):
    score = forms.IntegerField(
        min_value=0, initial=0, widget=forms.HiddenInput()
    )
    word_count = forms.IntegerField(min_value=0, widget=forms.HiddenInput())
    correct_words = forms.IntegerField(min_value=0, widget=forms.HiddenInput())
