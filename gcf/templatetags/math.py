from django import template


def minus(value, arg):
    return value - arg


def divide(value, arg):
    return value / arg


register = template.Library()
register.filter('minus', minus)
register.filter('divide', divide)
