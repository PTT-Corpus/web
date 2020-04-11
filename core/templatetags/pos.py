"""Concordance POS filter."""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='pos', takes_context=True)
def pos(str_value):
    result = ""

    if str_value == '':
        return str_value

    split_by_bar = str_value.split(' ')
    for word_pos in split_by_bar:
        word_pos = word_pos.split("##", 1)
        word = word_pos[0]
        pos = word_pos[1]
        result += f'{word}<span class="pos">{pos}</span>'
    return mark_safe(result)
    # for (index, item) in enumerate(split_by_bar):
    #     if index == 0 or index == len(split_by_bar) - 1:
    #         continue
    #     [pos, word] = split_by_bar[index].split('*^-', 1)
    #     split_by_bar[index] = "<span class=\"pos\">{}</span>{}".format(pos, word)
    # last_element = split_by_bar[len(split_by_bar) - 1]
    # split_by_bar[len(split_by_bar) - 1] = "<span class=\"pos\">{}</span>".format(last_element)
    # return mark_safe(''.join(split_by_bar))
