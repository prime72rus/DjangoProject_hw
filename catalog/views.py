from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.contrib import messages
from catalog.models import Product, Category
from catalog.forms import ProductForm
from django.core.paginator import Paginator


def home(request):
    products = Product.objects.all()
    top_5 = Category.objects.order_by('-category_name')[:5]
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "top_category": top_5,
        "page_obj": page_obj,
        "paginator": paginator
    }
    return render(request, "catalog/home.html", context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(
            f"Контактные данные и сообщение получены: "
            f"Ваше имя: {name}, номер телефона: {phone}, сообщение: {message}"
        )
    return render(request, "catalog/contacts.html")


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    referer = request.META.get('HTTP_REFERER', reverse("catalog:home"))
    context = {
        "product": product,
        "referer": referer
    }
    return render(request, "catalog/product_detail.html", context)


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продукт успешно добавлен!')
            return redirect('/add_product/')  # Перенаправляем на ту же страницу
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ProductForm()

    return render(request, 'catalog/add_product.html', {'form': form})
