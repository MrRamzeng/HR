from django import template
from main.models import Content

register = template.Library()


@register.simple_tag
def get_progress(book_id, reminder):
    count = Content.objects.filter(type__book_id=book_id).count()
    print(count, reminder)
    return f'{100 / count * (count - reminder)}%'
