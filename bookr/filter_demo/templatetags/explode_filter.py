from django import template

register = template.Library()

@register.filter
def explode(value, seperator):
    return value.split(seperator)