from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class AccuracyGame(models.Model):
    user = models.ForeignKey('user.User', models.CASCADE)
    timer = models.PositiveSmallIntegerField('Таймер', default=60)
    score = models.PositiveSmallIntegerField(default=0)
    accuracy = models.DecimalField(
        validators=(MinValueValidator(0), MaxValueValidator(100)), max_digits=5,
        decimal_places=2, default=0
    )
    W = 'Только слова'
    D = 'Только числа'
    S = 'Только знаки'
    ALL = 'Все'
    MODES = (
        (W, 'Только слова'),
        (D, 'Только числа'),
        (S, 'Только знаки'),
        (ALL, 'Все')
    )
    mode = models.CharField('Режим', choices=MODES, default=W, max_length=20)
    speed = models.PositiveSmallIntegerField('Количество символов', default=0)
    max_score = models.PositiveSmallIntegerField('Лучший счёт', default=0)
    best_accuracy = models.DecimalField(
        'лучшая аккуратность', max_digits=5, decimal_places=2,
        validators=(MinValueValidator(0), MaxValueValidator(100)), default=0
    )
    max_speed = models.PositiveSmallIntegerField(default=0)
    best_score_time = models.DateTimeField(blank=True, null=True)
    is_win = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.timer} {self.user.username}'

    class Meta:
        ordering = (
            '-max_score', '-max_speed', '-best_accuracy', '-best_score_time'
        )
