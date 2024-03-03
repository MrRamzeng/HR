from django import template
from main.models import Content

register = template.Library()


@register.simple_tag
def get_progress(pages, page):
    if page + 1 == pages:
        return '100%'
    return f'{int(page * 100 / pages)}%'
