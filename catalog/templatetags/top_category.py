from django import template
from catalog.models import Category

register = template.Library()

@register.inclusion_tag('catalog/includes/inc_category.html')
def show_category():
    top_category = Category.objects.order_by('-category_name')[:5]
    return {'top_category': top_category}
