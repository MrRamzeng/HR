from django.urls import path

from . import views

urlpatterns = [
    path(
        'accuracy/leaderboard/<str:mode>/', views.leaderboard,
        name='leaderboard'
    ),
    path('accuracy/', views.game, name='accuracy')
]
