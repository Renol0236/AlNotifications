from django import template

register = template.Library()

# Template Tags

@register.simple_tag
def is_active(request, view_name):
    return 'class="active"' if request.resolver_match.view_name == view_name else ''