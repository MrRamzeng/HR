from django import template

register = template.Library()


@register.simple_tag
def get_progress(pages, page):
    if page + 1 == pages:
        return '100%'
    return f'{int(page * 100 / pages)}%'
