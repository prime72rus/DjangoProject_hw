from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from catalog.models import Product, Category
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.forms import ProductForm, ProductModeratorForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from users.models import User
from django.core.exceptions import PermissionDenied
from django.core.cache import cache
from django.utils.decorators import method_decorator
from config.settings import CACHE_ENABLED
from catalog.services import ProductService


class ProductListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    paginate_by = 3

    def get_queryset(self):
        if not CACHE_ENABLED:
            return super().get_queryset()

        page = self.request.GET.get("page", 1)
        cache_key = f"product_list_queryset_{page}"
        queryset = cache.get(cache_key)

        if queryset is None:
            queryset = super().get_queryset()
            cache.set(cache_key, queryset, timeout=60 * 5)
        return queryset

class ProductByCategoryListView(ListView):

    model = Product
    template_name = "catalog/product_list_by_category.html"
    context_object_name = "products"
    paginate_by = 3

    def get_queryset(self):

        category_id = self.kwargs['pk']
        self.category = get_object_or_404(Category, id=category_id)

        if not CACHE_ENABLED:
            return ProductService.get_product_list_by_category(category_id)

        page = self.request.GET.get("page", 1)
        cache_key = f"product_list_by_category_{category_id}_page_{page}"  # Добавил category_id в ключ
        queryset = cache.get(cache_key)

        if queryset is None:
            queryset = ProductService.get_product_list_by_category(category_id)
            cache.set(cache_key, queryset, timeout=60 * 5)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


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

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm("catalog.can_unpublish_product"):
            raise PermissionDenied("У вас нет доступа к этой функции!")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("catalog:product_detail", kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    permission_required = "catalog.change_product"
    template_name = "catalog/product_form_update.html"

    def get_success_url(self):
        return reverse("catalog:product_detail", kwargs={'pk': self.object.pk})

    def has_permission(self):
        return (super().has_permission() or
                self.request.user.has_perm("catalog.can_unpublish_product"))

    def get_form_class(self):
        user = self.request.user
        if user.has_perm("catalog.can_unpublish_product"):
            return ProductModeratorForm
        else:
            return ProductForm


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    permission_required = "catalog.delete_product"
    success_url = reverse_lazy("catalog:home")
