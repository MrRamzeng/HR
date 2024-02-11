from django.db import models
from django.utils.safestring import mark_safe


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
        return self.name[:511]

    def html_text(self):
        text = self.text
        index = 0
        space_idx = 0
        tags = []
        # todo: edit
        for tag in list(text):
            if tag == '\r':
                tags.append('<span>&para;\n</span>')
                index = 0
            elif tag == '\n':
                continue
            elif tag == ' ':
                tags.append(f'<span>{tag}</span>')
                if index < 99:
                    space_idx = len(tags) - 1
                    index += 1
                else:
                    tags[space_idx] = f'<span>{tag}<br></span>'
                    index = len(tags[space_idx:])
            else:
                tags.append(f'<span>{tag}</span>')
                index += 1
        return mark_safe(''.join(tags))
