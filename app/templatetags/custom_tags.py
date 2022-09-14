from django import template
register = template.Library()

@register.filter
def calculateDiscount(value, arg):
    return round(value-(arg/100)*value,2)