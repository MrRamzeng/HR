from django import forms
from .models import AccuracyGame


class GameForm(forms.Form):
    TIMERS = (
        (30, "0:30"),
        (60, "1:00"),
        (120, "2:00")
    )
    mode = forms.ChoiceField(
        choices=AccuracyGame.MODES, label='Режим',
        widget=forms.RadioSelect(
            attrs={
                'onChange': 'setContent(this.value)'
            }
        ), initial=AccuracyGame.W
    )
    timer = forms.ChoiceField(
        choices=TIMERS, label='Таймер', initial=TIMERS[0],
        widget=forms.Select(
            attrs={
                'onChange': 'setTimer()'
            }
        )
    )
    score = forms.IntegerField(min_value=0, widget=forms.HiddenInput())
    accuracy = forms.DecimalField(
        max_value=100, min_value=0, decimal_places=2,
        max_digits=5, widget=forms.HiddenInput()
    )
    speed = forms.IntegerField(min_value=0, widget=forms.HiddenInput())
