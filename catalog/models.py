from django.db import models
from users.models import User


class Category(models.Model):
    category_name = models.CharField(max_length=150, verbose_name="Категория", unique=True)
    category_description = models.TextField(verbose_name="Описание категории")

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    product_name = models.CharField(max_length=150, verbose_name="Наименование")
    product_description = models.TextField(verbose_name="Описание продукта")
    image = models.ImageField(upload_to="images/", verbose_name="Изображение продукта", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="Категория")
    price = models.IntegerField(verbose_name="Цена, руб.")
    created_at = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateField(verbose_name="Дата последнего изменения", auto_now=True)
    is_public = models.BooleanField(default=False, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        permissions = [
            ("can_unpublish_product", "Сan unpublish product"),
        ]

