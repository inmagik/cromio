from django.contrib import admin

from .models import Product, ProductPrice

admin.site.register(Product)
admin.site.register(ProductPrice)
