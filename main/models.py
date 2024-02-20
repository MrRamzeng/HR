from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    author = models.CharField('Автор', max_length=50)
    name = models.CharField('Название', max_length=50)
    debug = models.BooleanField('Отладка', default=True)
    published = models.DateField('Дата публикации')

    class Meta:
        verbose_name_plural = 'книги'
        verbose_name = 'книга'

    def __str__(self):
        return self.name


# class Chapter(models.Model):
#     book = None
#     name = None
    # ...
    # ...
    # ...


class Tag(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    name = models.CharField('HTML тэг', max_length=10)
    src = models.TextField('источник', blank=True, null=True)
    css = models.CharField('Css', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'типы текста'
        verbose_name = 'тип текста'

    def __str__(self):
        return f'{self.name}'


class Content(models.Model):
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    text = models.TextField(verbose_name=None, blank=True, null=True)

    def get_text_length(self):
        return len(self.text)


class Printing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    content = models.ManyToManyField('Content', blank=True)
    # todo: edit
    position = models.PositiveIntegerField('Позиция', default=0)

    class Meta:
        verbose_name_plural = 'книги'
        verbose_name = 'книга'

    def __str__(self):
        return f'{self.book.name}, pos: {self.position}'
