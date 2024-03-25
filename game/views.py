from django.shortcuts import render, redirect
from datetime import datetime
from random import shuffle

from .forms import GameForm
from .words import words
from .models import AccuracyGame


def shuffle_words(list, ):
    shuffle(words)
    string = ''
    string_len = 0
    for word in words:
        if len(string) < 10000:
            word_len = len(word) + 1
            if string_len + word_len < 80:
                string += f'{word} '
                string_len += word_len
            else:
                string += f'{word}\n'
                string_len = 0
        else:
            break
    return string


def game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            timer = form.cleaned_data.get('timer')
            result, is_created = AccuracyGame.objects.get_or_create(
                user_id=(request.user.id or 1), timer=timer
            )
            result.timer = timer
            result.score = form.cleaned_data.get('score')
            result.accuracy = form.cleaned_data.get('accuracy')
            result.speed = form.cleaned_data.get('speed')
            if request.user.is_anonymous or result.score > result.max_score:
                result.max_score = result.score
                result.max_speed = result.speed
                result.best_accuracy = result.accuracy
                result.best_score_time = datetime.now()
            if request.user.is_authenticated and 1000 // 60 < result.speed:
                result.is_win = True
            result.save()
            return redirect('leaderboard')
    else:
        form = GameForm(
            initial={
                'score': 0,
                'accuracy': 0,
                'speed': 0
            }
        )
    return render(
        request, 'game/accuracy.html', {
            'form': form,
            'words': shuffle_words(words)
        }
    )


def leaderboard(request):
    position = None
    if request.user.is_anonymous:
        results = AccuracyGame.objects.filter(max_score__gt=0)[:3]
        user_id = 1
    else:
        results = AccuracyGame.objects.exclude(user_id=1).filter(
            max_score__gt=0
        )[:3]
        user_id = request.user.id
    result = AccuracyGame.objects.filter(user_id=user_id)
    if result and result not in results:
        results = results | result
        position = AccuracyGame.objects.exclude(user_id=1).filter(
            max_score__gte=result.first().max_score
        ).count()
    return render(
        request, 'game/leaderboard.html', {
            'results30': results.filter(timer=30),
            'results60': results.filter(timer=60),
            'results120': results.filter(timer=120),
            'position': position or 0
        }
    )
