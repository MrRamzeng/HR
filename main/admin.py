from django.contrib import admin
from .models import Book, Printing, Tag, Content
import nested_admin
from django.db import models
from django import forms

form_preset = {
    models.TextField: {
        'widget': forms.Textarea(
            attrs={
                'rows': 4,
                'cols': 100
            }
        )
    }
}

admin.site.register(Printing)


class ContentInline(nested_admin.NestedStackedInline):
    formfield_overrides = form_preset
    model = Content
    verbose_name_plural = 'Text'
    help_text = None
    extra = 1
    max_num = 1

    class Media:
        css = {
            'all': ('css/custom_admin.css',)
        }


class TagInline(nested_admin.NestedStackedInline):
    formfield_overrides = form_preset
    model = Tag
    extra = 1
    inlines = [ContentInline]

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Book)
class BookAdmin(nested_admin.NestedModelAdmin):
    formfield_overrides = form_preset
    inlines = [TagInline]
