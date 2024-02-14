from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User


class Book(models.Model):
    author = models.CharField('Автор', max_length=50)
    name = models.CharField('Название', max_length=50)
    published = models.DateField('Дата публикации')
    text = models.TextField('Текст')

    class Meta:
        verbose_name_plural = 'книги'
        verbose_name = 'книга'

    def __str__(self):
        return self.name

    def tags(self, position=0):
        text = self.text[position:]
        index = 0
        space_idx = 0
        tags = []

        for char in list(text):
            if char == '\r':
                tags.append('<span>&para;\n</span>')
                index = 0
            elif char == '\n':
                continue
            elif char == ' ':
                tags.append(f'<span>{char}</span>')
                if index >= 99:
                    tags[space_idx] = f'<span>{char}<br></span>'
                    index = len(tags[space_idx + 1:])
                space_idx = len(tags) - 1
            else:
                tags.append(f'<span>{char}</span>')
            index += 1
        return tags


class Printing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(
        'Book',
        on_delete=models.CASCADE,
        verbose_name='Книга'
    )
    position = models.PositiveIntegerField('Позиция', default=0)
    is_finished = models.BooleanField('Закончена', default=False)

    class Meta:
        verbose_name_plural = 'книги'
        verbose_name = 'книга'

    def __str__(self):
        return f'{self.book.name}, pos: {self.position}'

    def text(self):
        return mark_safe(''.join(self.book.tags(self.position)))
