from django.db import models


# Create your models here.
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
