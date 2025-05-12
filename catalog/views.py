from django.shortcuts import render
from django.http import HttpResponse

from catalog.models import Product


def home(request):
    sorted_products = Product.objects.order_by('created_at')
    for i in range(5):
        print(sorted_products[i])
    return render(request, "catalog/home.html")


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
