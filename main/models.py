from django.db import models
from django.contrib.auth.models import User


def image_path(instance, file):
    print(dir(instance))
    return f'{instance}/{file}'


class Font(models.Model):
    name = models.CharField('Шрифт', max_length=50)
    file = models.FileField('Файл')


class Book(models.Model):
    author = models.CharField('Автор', max_length=50)
    image = models.ImageField('Обложка', upload_to=image_path)
    name = models.CharField('Название', max_length=50)
    published = models.DateField('Дата публикации')
    font_family = models.ForeignKey(
        'Font', models.SET_NULL, blank=True, null=True
    )
    debug = models.BooleanField('Отладка', default=True)

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
    name = models.CharField('HTML тэг', max_length=10)

    def __str__(self):
        return self.name


class Paragraph(models.Model):
    book = models.ForeignKey('Book', models.CASCADE)
    tag = models.ForeignKey(
        'Tag', models.SET_NULL, blank=True, null=True
    )
    src = models.FileField('источник', blank=True, null=True)
    css = models.CharField('Css', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'абзацы'
        verbose_name = 'абзац'

    def __str__(self):
        return f'{self.tag.name}'


class Content(models.Model):
    type = models.ForeignKey('Paragraph', models.CASCADE)
    text = models.TextField(verbose_name=None, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'тексты'
        verbose_name = 'текст'

    def __str__(self):
        return str(self.id)

    # def get_text_length(self):
    #     return len(self.text)


class Printing(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    book = models.ForeignKey('Book', models.CASCADE)
    content = models.ManyToManyField('Content', blank=True)
    # todo: edit
    position = models.PositiveIntegerField('Позиция', default=0)

    class Meta:
        verbose_name_plural = 'книги'
        verbose_name = 'книга'

    def __str__(self):
        return f'{self.book.name}, pos: {self.position}'
