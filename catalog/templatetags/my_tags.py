from django import template
# from catalog.models import Category
# from blog.models import Post


register = template.Library()

@register.filter
def media_filter(path):
    if path:
        return f"/media/{path}"
    return "#"
