from django import template
from datetime import date
import os

register = template.Library()

@register.filter
def date_diff(value, arg):
    if isinstance(value, date) and isinstance(arg, date):
        delta = value - arg
        return delta.days
    return None

@register.filter
def filename(value):
    # Extracts just the filename from a path
    return os.path.basename(value)