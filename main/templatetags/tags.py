from django import template
from main.models import Book
register = template.Library()


@register.simple_tag
def get_progress(book_id, position):
    book = Book.objects.get(id=book_id)
    return f'{round(position * 100 / len(book.text))}%'
