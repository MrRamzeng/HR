from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    Author, Book, Paragraph, Content, Tag, Country, BookSeries, Genre,
    BookPage, Reading
)
import nested_admin
from django.db import models
from django import forms

form_preset = {
    models.TextField: {
        'widget': forms.Textarea(
            attrs={
                'rows': 10,
                'cols': 110
            }
        )
    }
}


def img(obj):
    return mark_safe(
        f'<img src="{obj.image.url}" width="142px" height="213px"/>'
    )


def page(obj):
    return mark_safe(
        f'<img src="{obj.image.url}" width="852px" height="1272px"/>'
    )


@admin.register(Author)
class AuthorAdmin(nested_admin.NestedModelAdmin):
    formfield_overrides = form_preset
    readonly_fields = [img]
    fieldsets = [
        ('Title', {
            'fields': [
                ('last_name', 'first_name', 'patronymic', 'pseudonym',
                 'country'),
                ('date_of_birth', 'date_of_death'),
                ('image', img, 'biography'),
            ],
        }),
    ]
    img.short_description = 'Предпросмотр'


admin.site.register(Country)
admin.site.register(Reading)
admin.site.register(Tag)
admin.site.register(Genre)
admin.site.register(BookSeries)


class ContentInline(nested_admin.NestedTabularInline):
    formfield_overrides = form_preset
    model = Content
    extra = 1
    max_num = 1


class ParagraphInline(nested_admin.NestedTabularInline):
    formfield_overrides = form_preset
    # ordering = ('-id',)
    model = Paragraph
    extra = 0
    inlines = [ContentInline]
    # template = 'inlines/tabular.html'

    # def has_delete_permission(self, request, obj=None):
    #     return False


class PageInline(nested_admin.NestedTabularInline):
    model = BookPage
    extra = 1
    readonly_fields = [page]


@admin.register(Book)
class BookAdmin(nested_admin.NestedModelAdmin):
    formfield_overrides = form_preset
    inlines = [ParagraphInline, PageInline]
    readonly_fields = [img]
    fieldsets = [
        ('Title', {
            'fields': [
                ('name', 'published', 'series', 'series_number', 'font_family'),
                ('authors', 'genre'),
                ('image', img, 'description'),
                ('price', 'sale'),
                'debug'
            ],
        }),
    ]
    img.short_description = 'Предпросмотр'

    class Media:
        css = {
            'all': ('css/custom_admin.css',)
        }
        js = ['scripts/admin_scroll.js']
