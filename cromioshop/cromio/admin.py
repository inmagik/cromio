from django.contrib import admin

from .models import Product, ProductPrice, Support

admin.site.register(Support)
admin.site.register(Product)
admin.site.register(ProductPrice)
