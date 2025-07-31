from django import template

register = template.Library()

@register.filter(name='unit')
def unit(data, args):
    return data+" MM"
