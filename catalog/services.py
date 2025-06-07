from catalog.models import Product, Category


class ProductService:

    @staticmethod
    def get_product_list_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
            return category.products.all()
        except ObjectDoesNotExist:
            return Product.objects.none()