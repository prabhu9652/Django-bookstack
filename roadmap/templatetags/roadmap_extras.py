from django import template

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """
    Template filter to lookup dictionary values by key
    Usage: {{ dict|lookup:key }}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key, {})
    return {}

@register.filter
def widthratio_safe(value, max_value, scale):
    """
    Safe version of widthratio that handles None values
    """
    if value is None or max_value is None or max_value == 0:
        return 0
    try:
        return int((value / max_value) * scale)
    except (TypeError, ZeroDivisionError):
        return 0