from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import Case, When, IntegerField
from django.utils.safestring import mark_safe

from .models import (
    Author, Book, Content, Country, BookSeries, Genre,
    BookFile, UserBooks, Footnote
)
import nested_admin
from django.db import models
from django import forms
from django_admin_inline_paginator.admin import TabularInlinePaginated

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
admin.site.register(UserBooks)
admin.site.register(Genre)
admin.site.register(BookSeries)
admin.site.register(Footnote)


class PageInline(nested_admin.NestedTabularInline):
    model = BookFile
    extra = 1


class FootnoteInline(nested_admin.NestedTabularInline):
    model = Footnote
    # exclude = ('id')
    extra = 0


class ContentInline(nested_admin.NestedTabularInline, TabularInlinePaginated):
    model = Content
    inlines = [FootnoteInline]
    template = 'admin/inlines/grappelli_tabular.html'
    exclude = ('id', 'text_len')
    extra = 0
    per_page = 10

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     queryset = queryset.annotate(
    #         tag_hierarchy=Case(
    #             When(tag='img', then=0),
    #             When(tag='header', then=1),
    #             When(tag='h1', then=2),
    #             default=3,
    #             output_field=IntegerField()
    #         )
    #     ).order_by('tag_hierarchy', 'id')
    #     return queryset


@admin.register(Book)
class BookAdmin(nested_admin.NestedModelAdmin):
    inlines = [PageInline, ContentInline]
    readonly_fields = [img]
    fieldsets = [
        ('О книге', {
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
        # css = {
        #     'all': ('css/custom_admin.css',)
        # }
        js = ['scripts/admin_scroll.js']