from django.db import models


class AccuracyResult(models.Model):
    user = models.ForeignKey('user.User', models.CASCADE)
    last_word_count = models.PositiveSmallIntegerField(
        'Количество слов', blank=True, null=True
    )
    last_correct_words = models.PositiveSmallIntegerField(
        'Количество слов без ошибок', blank=True, null=True
    )
    last_score = models.PositiveSmallIntegerField(
        'Счёт', blank=True, null=True
    )
    best_score = models.PositiveSmallIntegerField(
        'Лучший счёт', default=0
    )
    best_score_time = models.DateTimeField(
        'Время лучшего счета', blank=True, null=True
    )

    def __str__(self) -> str:
        return f'{self.user.username} {self.best_score}'
    
    class Meta:
        ordering = '-best_score', '-best_score_time'
