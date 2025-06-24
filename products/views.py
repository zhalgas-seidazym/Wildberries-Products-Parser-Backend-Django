from rest_framework import generics, filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer
from .filters import ProductFilter
from .services import ParserService, ProductService
from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 200


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, drf_filters.OrderingFilter]
    ordering_fields = ["price", "sale_price", "rating", "feedbacks"]
    ordering = ["-rating"]

    def get_queryset(self):
        query = self.request.query_params.get("query")
        if not query:
            return Product.objects.none()
        print("query", query)

        parser = ParserService()
        product_service = ProductService(parser)
        search_obj = product_service.refresh_search_query(query)
        return search_obj.products.all()
