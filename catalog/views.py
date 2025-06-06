from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib import messages
from catalog.models import Product, Category
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User

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


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form_create.html"

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form_update.html"

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy('catalog:home')
