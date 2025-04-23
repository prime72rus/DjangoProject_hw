from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name",)
    search_fields = ("category_name", "category_description",)



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "price", "category",)
    search_fields = ("product_name", "product_description",)
    list_filter = ("category",)