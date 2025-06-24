from django.contrib import admin

from products.models import Product, SearchQuery

admin.site.register(Product)
admin.site.register(SearchQuery)