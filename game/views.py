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
                    and result.accuracy > result.best_accuracy
                    and result.speed > result.max_speed):
                result.max_score = result.score
                result.max_speed = result.speed
                result.best_accuracy = result.accuracy
                result.best_score_time = datetime.now()
            if int(result.timer) <= 60 and 1000 // 60 < result.speed:
                result.is_win = True
            result.save()
            return redirect('leaderboard', mode)
    else:
        form = GameForm(initial={'score': 0, 'accuracy': 0, 'speed': 0})
    return render(request, 'game/accuracy.html', {'form': form})


def set_position(results, user):
    fields = [
        'timer', 'user__username', 'max_score', 'max_speed', 'best_accuracy'
    ]
    if user.is_authenticated:
        top_users = results.values_list('user__username', flat=True)[:10]
        print(top_users)
        if user in top_users:
            return list(results.values(*fields)[:10])
        elif results.filter(user=user).exists():
            result = results.filter(user=user).values(*fields).first()
            print(result, dir(result))
            result['position'] = results.filter(
                best_accuracy__gte=float(result['best_accuracy'])
            ).count()
            results = list(results.values(*fields)[:9])
            results.append(result)
            print(results)
            return results
    return list(results.values(*fields)[:10])


def leaderboard(request, mode):
    results30 = set_position(
        AccuracyGame.objects.filter(mode=mode, timer=30),
        request.user
    )

    results60 = set_position(
        AccuracyGame.objects.filter(mode=mode, timer=60),
        request.user
    )
    results120 = set_position(
        AccuracyGame.objects.filter(mode=mode, timer=120),
        request.user
    )
    return render(
        request,
        'game/leaderboard.html',
        {
            'results30': results30,
            'results60': results60,
            'results120': results120
        }
    )
