from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib import messages
from catalog.models import Product, Category
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class ProductListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    paginate_by = 3


class ContactsView(View):
    template_name = "catalog/contacts.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(
            f"Контактные данные и сообщение получены: "
            f"Ваше имя: {name}, номер телефона: {phone}, сообщение: {message}"
        )


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['referer'] = self.request.META.get(
            'HTTP_REFERER',
            reverse("catalog:home")
        )
        return context


class ProductCreateView(CreateView):
    model = Product
    fields = ["product_name", "product_description", "image", "category", "price"]
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy('catalog:product_create')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Продукт успешно добавлен!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)
