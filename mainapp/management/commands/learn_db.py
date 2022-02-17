from time import time

from django.core.management.base import BaseCommand
from mainapp.models import Product
from django.db.models import Q


class Command(BaseCommand):
    def handle(self, *args, **options):
        """ Вариант или, поиск продукта по категории или по ID"""
        # products = Product.objects.filter(
        #    Q(category__name='Обувь') | Q(id=18))
        """ Вариант при 2-х условиях 'и', поиск продукта по категории и ID."""
        products = Product.objects.filter(
           Q(category__name='Обувь') & Q(id=5))
        """ Вариант при установки символа ~ выбор все за исключение указаной категории """
        # products = Product.objects.filter(
        #    ~Q(category__name='Обувь'))
        # products = Product.objects.filter(
        #    ~Q(category__name='Обувь'), id=4)
        print(products)
