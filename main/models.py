from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from user.models import User
from HandRead.storage import OverwriteStorage


def file_path(instance, file):
    return f'{instance._meta.verbose_name_plural}/{instance}/{file}'


def page_path(instance, file):
    return (f'{instance.book._meta.verbose_name_plural}/{instance.book.name}/'
            f'{instance._meta.verbose_name_plural}/{file}')


class Country(models.Model):
    name = models.CharField('Название', max_length=20)
    image = models.ImageField(
        'Флаг', storage=OverwriteStorage(), upload_to=file_path
    )

    class Meta:
        verbose_name_plural = 'страны'
        verbose_name = 'страна'

    def __str__(self):
        return self.name


class Author(models.Model):
    last_name = models.CharField('Фамилия', max_length=20)
    first_name = models.CharField('Имя', max_length=20)
    patronymic = models.CharField(
        'Отчество', max_length=20, blank=True, null=True
    )
    pseudonym = models.CharField(
        'Псевдоним', max_length=20, blank=True, null=True
    )
    image = models.ImageField(
        'Фото', storage=OverwriteStorage(), upload_to=file_path
    )
    biography = models.TextField('Биография')
    date_of_birth = models.DateField('Дата рождения')
    date_of_death = models.DateField(
        'Дата смерти', blank=True, null=True
    )
    country = models.ManyToManyField('Country', verbose_name='Гражданство')

    class Meta:
        verbose_name_plural = 'авторы'
        verbose_name = 'автор'

    def __str__(self):
        return f'{self.pseudonym or self.get_full_name()}'

    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=50)

    class Meta:
        verbose_name_plural = 'жанры'
        verbose_name = 'жанр'

    def __str__(self):
        return self.name


class Font(models.Model):
    name = models.CharField('Шрифт', max_length=50)
    file = models.FileField(
        'Файл', storage=OverwriteStorage(), upload_to=file_path
    )

    class Meta:
        verbose_name_plural = 'шрифты'
        verbose_name = 'шрифт'

    def __str__(self):
        return self.name


class BookSeries(models.Model):
    name = models.CharField('Название серии', max_length=50)

    class Meta:
        verbose_name_plural = 'серии'
        verbose_name = 'серия'


class Book(models.Model):
    name = models.CharField('Название', max_length=50)
    authors = models.ManyToManyField('Author', 'Авторы')
    image = models.ImageField(
        'Обложка', storage=OverwriteStorage(), upload_to=file_path
    )
    description = models.TextField('Описание')
    published = models.DateField('Дата публикации')
    font_family = models.ForeignKey(
        'Font', models.SET_NULL, blank=True, null=True
    )
    genre = models.ManyToManyField('Genre', verbose_name='Жанр')
    price = models.PositiveSmallIntegerField('Цена', default=100)
    sale = models.PositiveSmallIntegerField(
        'Скидка %', validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    series = models.ForeignKey(
        'BookSeries', models.CASCADE, verbose_name='Серия', blank=True,
        null=True
    )
    series_number = models.SmallIntegerField(
        'Номер серии', blank=True, null=True
    )
    # languages = models.ManyToManyField('Language', verbose_name='Языки')
    debug = models.BooleanField('Отладка', default=True)

    class Meta:
        verbose_name_plural = 'книги'
        verbose_name = 'книга'

    def __str__(self):
        return self.name


class BookPage(models.Model):
    book = models.ForeignKey('Book', models.CASCADE)
    A4 = 'A4'
    A6 = 'A6'
    SIZES = (
        (A4, 'A4'),
        (A6, 'A6'),
    )
    size = models.CharField(
        'Размер', max_length=10, choices=SIZES, default=A4
    )
    image = models.ImageField(
        'Файл книги', storage=OverwriteStorage(), upload_to=page_path
    )

    class Meta:
        verbose_name_plural = 'страницы'
        verbose_name = 'страница'


# class Chapter(models.Model):
#     book = None
#     name = None
# ...
# ...
# ...


class Paragraph(models.Model):
    book = models.ForeignKey('Book', models.CASCADE)
    P = 'p'
    H1 = 'h1'
    H2 = 'h2'
    H3 = 'h3'
    H4 = 'h4'
    H5 = 'h5'
    I = 'i'
    IMG = 'img'
    TAGS = (
        (H1, 'h1'),
        (H2, 'h2'),
        (H3, 'h3'),
        (H4, 'h4'),
        (H5, 'h5'),
        (I, 'i'),
        (IMG, 'img'),
        (P, 'p'),
    )
    tag = models.CharField(
        'Тег', choices=TAGS, default=P, max_length=20
    )
    src = models.FileField(
        'источник', storage=OverwriteStorage(), upload_to=file_path,
        blank=True, null=True
    )
    css = models.CharField('Css', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'абзацы'
        verbose_name = 'абзац'

    def __str__(self):
        return f'{self.tag}'



class Content(models.Model):
    type = models.ForeignKey('Paragraph', models.CASCADE)
    text = models.TextField('Текст', blank=True, null=True)
    text_len = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'тексты'
        verbose_name = 'текст'

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.text_len = len(self.text)
        return super(Content, self).save(*args, **kwargs)


class UserBooks(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    book = models.ForeignKey('Book', models.CASCADE)
    # todo: edit
    typing_position = models.PositiveIntegerField(
        validators=[MinValueValidator(0)], default=0
    )
    page_position = models.PositiveIntegerField(
        validators=[MinValueValidator(0)], default=0
    )
    has_read = models.BooleanField(default=False)
    has_print = models.BooleanField(default=False)
    position = models.PositiveIntegerField(
        validators=[MinValueValidator(0)], default=0
    )

    class Meta:
        verbose_name_plural = 'чтение'
        verbose_name = 'чтение'

    def get_pages_count(self):
        return BookPage.objects.filter(book_id=self.book_id).count()

    def has_content(self):
        return Content.objects.filter(type__book_id=self.book_id).exists()

    def get_print_progress(self):
        count = Content.objects.filter(type__book_id=self.book_id).count()
        return int(self.typing_position * 100 / count)

    def __str__(self):
        return f'{self.book.name}'
