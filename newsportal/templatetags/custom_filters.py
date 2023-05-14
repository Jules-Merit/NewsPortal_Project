from django import template

register = template.Library()


@register.filter
def censor(value):
    bad_words = ['Samsung', 'выгодно', 'кожи']
    for bw in bad_words:
        value = value.replace(bw, '*' * len(bw))
    return value
