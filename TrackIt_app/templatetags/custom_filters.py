from django import template
from datetime import date

register = template.Library()

@register.filter
def date_diff(value, arg):
    """
    Calculate the difference in days between two dates.
    """
    if isinstance(value, date) and isinstance(arg, date):
        delta = value - arg
        return delta.days
    return None