from django.shortcuts import render, redirect
from datetime import datetime
from random import shuffle

from .forms import GameForm
from .words import words
from .models import AccuracyResult


def shuffle_words(list):
    shuffle(words)
    string = ''
    string_len = 0
    for word in words:
        if len(string) < 2000:
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
    result, is_created = AccuracyResult.objects.get_or_create(
        user_id=(request.user.id or 1)
    )
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            result.last_score = form.cleaned_data.get('score')
            result.last_word_count = form.cleaned_data.get('word_count')
            result.last_correct_words = form.cleaned_data.get('correct_words')
            result.best_score_time = datetime.now()
            if request.user.is_anonymous:
                result.best_score = result.last_score
            else:
                if result.last_score > result.best_score:
                    result.best_score = result.last_score
            result.save()
            return redirect('leaderboard')
    else:
        form = GameForm(
            initial={
                'last_word_count': 0,
                'last_correct_words': 0,
                'last_score': 0
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
        results = AccuracyResult.objects.filter(best_score__gt=0)[:3]
        user_id = 1
    else:
        results = AccuracyResult.objects.exclude(user_id=1).filter(
            best_score__gt=0
        )[:3]
        user_id = request.user.id
    result = AccuracyResult.objects.filter(user_id=user_id)
    if result not in results:
        results = results | result
        position = AccuracyResult.objects.exclude(user_id=1).filter(
            best_score__gte=result.first().best_score
        ).count()
    return render(
        request, 'game/leaderboard.html', {
            'results': results,
            'position': position
        }
    )
