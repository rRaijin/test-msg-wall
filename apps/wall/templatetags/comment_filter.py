from django import template


register = template.Library()

@register.filter
def parent_filter(obj):
    return obj.filter(parent=None)