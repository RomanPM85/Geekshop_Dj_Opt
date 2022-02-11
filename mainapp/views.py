from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

import json
import os

from django.views.generic import DetailView
from django.conf import settings
from django.core.cache import cache

from mainapp.models import Product, ProductCategory

MODULE_DIR = os.path.dirname(__file__)


# Create your views here.

def index(request):
    context = {
        'title': 'Geekshop', }
    return render(request, 'mainapp/index.html', context)


def get_link_category():
    if settings.LOW_CACHE:
        key = 'link_category'
        link_category = cache.get(key)
        if link_category is None:
            link_category = ProductCategory.objects.all()
            cache.set(key, link_category)
        return link_category
    else:
        return ProductCategory.objects.all()


def get_product():
    if settings.LOW_CACHE:
        key = 'link_product'
        link_product = cache.get(key)
        if link_product is None:
            link_product = Product.objects.all().select_related('category')
            cache.set(key, link_product)
        return link_product
    else:
        return Product.objects.all().select_related('category')


def products(request, id_category=None, page=1):

    context = {
        'title': 'Geekshop | Каталог',
    }

    if id_category:
        """
        добавляем select_related('category') для загрузки из сервера всех данных по категории,
        чтобы не обращаться каждый раз к серверу
        """
        products = Product.objects.filter(category_id=id_category).select_related('category')
    else:
        products = Product.objects.all().select_related()
        """
        добавляем prefetch_related если имеем связи многие ко многим
        """
        # products = Product.objects.all().prefetch_related()
        # products = get_product()
    paginator = Paginator(products, per_page=3)

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context['products'] = products_paginator
    # context['categories'] = ProductCategory.objects.all()
    context['categories'] = get_link_category()
    return render(request, 'mainapp/products.html', context)


class ProductDetail(DetailView):
    """
    Контроллер вывода информации о продукте
    """
    model = Product
    template_name = 'mainapp/detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super(ProductDetail, self).get_context_data(**kwargs)
    #     product = self.get_object()
    #     context['product'] = product
    #     return context

