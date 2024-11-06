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

@register.filter
def split_tracking_no(tracking_no):
    parts = tracking_no.split('-', 1)  # Split into two parts at the first hyphen
    return f"{parts[0]}-<br>{parts[1]}" if len(parts) > 1 else tracking_no