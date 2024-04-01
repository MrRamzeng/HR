from django import forms
from django.utils.safestring import mark_safe

from .models import AccuracyGame


class HorizRadioRenderer(forms.RadioSelect):
    def render(self):
            return mark_safe(u'\n'.join([u'%s\nalliluya' % w for w in self]))


class GameForm(forms.Form):
    TIMERS = (
        (30, "0:30"),
        (60, "1:00"),
        (120, "2:00")
    )
    mode = forms.ChoiceField(
        choices=AccuracyGame.MODES, label='Режим',
        widget=forms.Select(
            attrs={
                'onChange': 'setContent(this.value)', 'class': 'block p-2 mb-6 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"'
            }
        ), initial=AccuracyGame.W
    )
    timer = forms.ChoiceField(
        choices=TIMERS, label='Таймер', initial=TIMERS[0],
        widget=forms.Select(
            attrs={
                'onChange': 'setTimer()', 'class': 'block p-2 mb-6 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }
        )
    )
    score = forms.IntegerField(min_value=0, widget=forms.HiddenInput())
    accuracy = forms.DecimalField(
        max_value=100, min_value=0, decimal_places=2,
        max_digits=5, widget=forms.HiddenInput()
    )
    speed = forms.IntegerField(min_value=0, widget=forms.HiddenInput())
