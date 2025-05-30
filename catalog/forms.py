import os
from django import forms
from django.core.exceptions import ValidationError
from catalog.models import Product


EXCLUSION_WORDS = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]
MAX_UPLOAD_SIZE = 5 * 1024 * 1024
ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/jpg']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["product_name", "product_description", "image", "category", "price"]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields["product_name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите название продукта",
        })
        self.fields["product_description"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите описание продукта",
            "rows": 3,
        })
        self.fields["image"].widget.attrs.update({
            "class": "form-control",
            "accept": "image/*",
            "multiple": False,
        })
        self.fields["category"].widget.attrs.update({
            "class": "form-control",
        })
        self.fields["price"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите стоимость продукта",
        })

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if not image:
            return image

        ext = os.path.splitext(image.name)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png']:
            raise ValidationError('Недопустимое расширение файла. Используйте .jpg, .jpeg или .png.')

        if image.size > MAX_UPLOAD_SIZE:
            raise ValidationError('Размер файла не должен превышать 5 МБ.')

        return image

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        return price

    def clean(self):
        cleaned_data = super().clean()
        product_name = cleaned_data.get("product_name")
        product_description = cleaned_data.get("product_description")
        if any(sub in str(product_name).lower() for sub in EXCLUSION_WORDS):
            self.add_error("product_name", "Введено запрещенное слово")
        if any(sub in str(product_description).lower() for sub in EXCLUSION_WORDS):
            self.add_error("product_description", "Введено запрещенное слово")
