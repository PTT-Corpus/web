"""Concordance paginator."""
import math

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def paginator(context):
    """Pagingnator template tag."""
    size = context['data']['size']
    page = context['data']['page']
    total_pages = round(context['data']['total'] / size)
    start = math.floor(page / size) * size
    end = start + size
    if end >= total_pages:
        end = total_pages
    return range(start, end)


@register.simple_tag(takes_context=True)
def paging_prev(context):
    """Paging prev."""
    page = context['data']['page']
    size = context['data']['size']
    res = math.floor((page + 1) / size) - 1
    if res == -1:
        return None
    return res


@register.simple_tag(takes_context=True)
def paging_next(context):
    """Paging next."""
    page = context['data']['page']
    size = context['data']['size']
    total_pages = round(context['data']['total'] / size)
    res = (math.floor((page + 1) / size) * size) + size
    if res >= total_pages - 1:
        return None
    return res
