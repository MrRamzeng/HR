from django.shortcuts import render, redirect
from datetime import datetime

from .forms import GameForm
from .models import AccuracyGame


def game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            timer = form.cleaned_data.get('timer')
            mode = form.cleaned_data.get('mode')
            result, is_created = AccuracyGame.objects.get_or_create(
                user_id=request.user.id, timer=timer, mode=mode
            )
            result.timer = timer
            result.mode = mode
            result.score = form.cleaned_data.get('score')
            result.accuracy = form.cleaned_data.get('accuracy')
            result.speed = form.cleaned_data.get('speed')
            if (result.score > result.max_score
                    and result.accuracy > result.best_accuracy):
                result.max_score = result.score
                result.max_speed = result.speed
                result.best_accuracy = result.accuracy
                result.best_score_time = datetime.now()
            if 1000 // 60 < result.speed:
                result.is_win = True
            result.save()
            return redirect('leaderboard', mode)
    else:
        form = GameForm(initial={'score': 0, 'accuracy': 0, 'speed': 0})
    return render(request, 'game/accuracy.html', {'form': form})


def leaderboard(request, mode):
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
            'results30': results.filter(timer=30, mode=mode),
            'results60': results.filter(timer=60, mode=mode),
            'results120': results.filter(timer=120, mode=mode),
            'position': position or 0
        }
    )
