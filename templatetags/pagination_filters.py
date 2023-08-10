from django import template

register = template.Library()


@register.simple_tag
def url_field_replace(request, field, value):
    """Alter the request parameter `field` to `value` in the request URL."""
    query = request.GET.copy()
    query[field] = value
    return query.urlencode()
