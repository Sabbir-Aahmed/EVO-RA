from django import template
from datetime import datetime
from django.utils import timezone

register = template.Library()

@register.filter
def humanize_date(value):
    if value:
        today = datetime.now().date()
        value = timezone.localtime(value)
        if value.date() == today:
            return f"Today at {value.strftime('%I:%M %p')}"
        if value.date() == today.replace(day=today.day-1):
            return f"Yeasterday at {value.strftime('%I:%M %P')}"
        return value.strftime('%B %d, %Y at %I:%M %p')
    return "No login record available"