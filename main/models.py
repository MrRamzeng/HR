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

    def html_text(self):
        text = self.text
        index = 0
        space_idx = 0
        tags = []

        for symbol in list(text):
            if symbol == '\r':
                tags.append('<span>&para;\n</span>')
                index = 0
            elif symbol == '\n':
                continue
            elif symbol == ' ':
                tags.append(f'<span>{symbol}</span>')
                if index >= 99:
                    tags[space_idx] = f'<span>{symbol}<br></span>'
                    index = len(tags[space_idx + 1:])
                space_idx = len(tags) - 1
            else:
                tags.append(f'<span>{symbol}</span>')
            index += 1
        return mark_safe(''.join(tags))
