from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=150, verbose_name="Категория", unique=True)
    category_description = models.TextField(verbose_name="Описание категории")

    def __str__(self):
        return f"{self.category_name}\nОписание: {self.category_description}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    product_name = models.CharField(max_length=150, verbose_name="Наименование")
    product_description = models.TextField(verbose_name="Описание продукта")
    image = models.ImageField(upload_to="images/", verbose_name="Изображение продукта", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    price = models.IntegerField(verbose_name="Цена, руб.")
    created_at = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateField(verbose_name="Дата последнего изменения", auto_now=True)

    def __str__(self):
        return (f"{self.product_name}\nОписание: {self.product_description}\n"
                f"Категория: {self.category}\nЦена: {self.price} руб.")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
