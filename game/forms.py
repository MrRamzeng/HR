from django import forms

from .models import AccuracyGame


class GameForm(forms.Form):
    mode = forms.ChoiceField(
        choices=AccuracyGame.MODES, label='Режим',
        initial=AccuracyGame.MODES[0],
        widget=forms.RadioSelect(
            attrs={
                # 'id': 'mode',
                'onChange': 'setContent(this.value)',
                'type': 'radio',
                'name': 'timer',
                'class': 'hidden peer'
            }
        )
    )
    timer = forms.ChoiceField(
        choices=AccuracyGame.TIMERS, label='Таймер',
        initial=AccuracyGame.TIMERS[0],
        widget=forms.RadioSelect(
            attrs={
                # 'id': 'timer',
                'onChange': 'setPreset(this.id)',
                'type': 'radio',
                'name': 'timer',
                'class': 'hidden peer'
            }
        )
    )
    score = forms.IntegerField(min_value=0, widget=forms.HiddenInput())
    accuracy = forms.DecimalField(
        max_value=100, min_value=0, decimal_places=2,
        max_digits=5, widget=forms.HiddenInput()
    )
    speed = forms.IntegerField(min_value=0, widget=forms.HiddenInput())
