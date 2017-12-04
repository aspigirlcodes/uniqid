from django import template

register = template.Library()


@register.filter
def get_display_value(choices, request_key):
    for key, value in choices:
        if key == request_key:
            return value
    return ""
