from django.urls import path

from . import views

urlpatterns = [
    path('accuracy/leaderboard/', views.leaderboard, name='leaderboard'),
    path('accuracy/', views.game, name='accuracy')
]
