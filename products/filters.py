from django_filters import rest_framework as filters
from .models import Product

from django_filters import rest_framework as filters
from .models import Product

class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    min_sale_price = filters.NumberFilter(field_name="sale_price", lookup_expr="gte")
    max_sale_price = filters.NumberFilter(field_name="sale_price", lookup_expr="lte")
    min_rating = filters.NumberFilter(field_name="rating", lookup_expr="gte")
    min_reviews = filters.NumberFilter(field_name="feedbacks", lookup_expr="gte")

    class Meta:
        model = Product
        fields = [
            "min_price", "max_price",
            "min_sale_price", "max_sale_price",
            "min_rating", "min_reviews"
        ]
