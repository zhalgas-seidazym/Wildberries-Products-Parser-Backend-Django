from django.db import models
from django.utils import timezone
from datetime import timedelta


class Product(models.Model):
    product_id = models.BigIntegerField(primary_key=True, help_text="Уникальный ID товара на Wildberries")
    name = models.CharField(max_length=500)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    rating = models.FloatField(null=True, blank=True)
    feedbacks = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-rating", "-feedbacks"]
        indexes = [
            models.Index(fields=["price"]),
            models.Index(fields=["rating"]),
            models.Index(fields=["feedbacks"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.product_id})"


class SearchQuery(models.Model):
    query = models.CharField(max_length=255, unique=True)
    last_parsed = models.DateTimeField(auto_now=True)

    products = models.ManyToManyField(
        Product,
        through="QueryProduct",
        related_name="search_queries",
    )

    PARSE_INTERVAL = timedelta(hours=6)

    class Meta:
        ordering = ["-last_parsed"]

    def __str__(self):
        return f"{self.query} {self.last_parsed}"

    def needs_refresh(self) -> bool:
        return self.last_parsed < timezone.now() - self.PARSE_INTERVAL


class QueryProduct(models.Model):
    query = models.ForeignKey(SearchQuery, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("query", "product")
