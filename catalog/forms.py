from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_description', 'image', 'category', 'price']
        widgets = {
            'product_description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all().only('category_name')
        self.fields['category'].empty_label = "Выберите категорию"
        self.fields['category'].label = "Категория"