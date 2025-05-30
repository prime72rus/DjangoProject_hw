from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib import messages
from catalog.models import Product, Category
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.forms import ProductForm

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


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form_create.html"
    # success_url = reverse_lazy('catalog:home')

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form_update.html"

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    # form_class = ProductForm
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy('catalog:home')
