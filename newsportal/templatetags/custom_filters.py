from django import template

register = template.Library()


@register.filter
def censor(value):
    if not isinstance(value, str):
        raise ValueError('Value must be of string type')
    bad_words = ['Samsung', 'кожи', 'выгодно']
    for bw in bad_words:
        value = value.replace(bw, '*'*len(bw))
    return value
