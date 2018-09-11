"""Concordance POS filter."""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='pos', takes_context=True)
def pos(str_value):

    if str_value == '':
        return str_value

    split_by_bar = str_value.split('|')
    for (index, item) in enumerate(split_by_bar):
        if index == 0 or index == len(split_by_bar) - 1:
            continue
        [pos, word] = split_by_bar[index].split(' ', 1)
        split_by_bar[index] = "<span class=\"pos\">{}</span>{}".format(pos, word)
    last_element = split_by_bar[len(split_by_bar) - 1]
    split_by_bar[len(split_by_bar) - 1] = "<span class=\"pos\">{}</span>".format(last_element)
    return mark_safe(''.join(split_by_bar))
