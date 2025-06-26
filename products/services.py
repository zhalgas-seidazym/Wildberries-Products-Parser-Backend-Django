import json
import os
from datetime import datetime

from .models import Product, SearchQuery, QueryProduct
from django.utils import timezone
from django.db import transaction
import httpx
import time


class ParserService:
    BASE_URL = "https://search.wb.ru/exactmatch/sng/common/v13/search"
    HEADERS = {"User-Agent": "Mozilla/5.0"}

    def __init__(self, delay=0.2, max_pages=3, limit=100):
        self.delay = delay
        self.max_pages = max_pages
        self.limit = limit

    def parse(self, query: str) -> list[dict]:
        all_products = []

        for page in range(1, self.max_pages + 1):
            params = {
                "query": query,
                "page": page,
                "limit": self.limit,
                "resultset": "catalog",
                "spp": 30,
                "appType": 1,
                "dest": 1235851,
                "curr": "rub",
                "lang": "ru"
            }

            try:
                response = httpx.get(self.BASE_URL, params=params, headers=self.HEADERS, timeout=10)
                response.raise_for_status()

                data = response.json()
                metadata = data.get("metadata", {})

                if metadata.get("is_empty") is True:
                    print(f"[!] Empty result at page {page} — stopping.")
                    break

                products = data.get("data", {}).get("products", [])
                if not products:
                    print(f"[i] No products at page {page}, stopping.")
                    break


                for p in products:
                    price = p["sizes"][0]["price"]["basic"] / 100
                    sale_price = p["sizes"][0]["price"]["product"] / 100

                    all_products.append({
                        "product_id": p["id"],
                        "name": p["name"][:500],
                        "price": price,
                        "sale_price": sale_price,
                        "rating": p.get("reviewRating") or 0,
                        "feedbacks": p.get("feedbacks", 0),
                    })


                print(f"[+] Page {page}: loaded {len(products)} products")
                # time.sleep(self.delay)

            except Exception as e:
                print(f"[x] Error on page {page}: {e}")
                break

        return all_products


class ProductService:
    def __init__(self, parser_service: ParserService):
        self.parser = parser_service

    def refresh_search_query(self, query: str) -> SearchQuery:

        try:
            search_obj = SearchQuery.objects.get(query=query)
        except SearchQuery.DoesNotExist:
            search_obj = None

        if search_obj and not search_obj.needs_refresh():
            return search_obj
        else:
            search_obj, _ = SearchQuery.objects.get_or_create(query=query)

        print(f"[*] Updating search query: {query}")
        parsed_data = self.parser.parse(query)
        print('Data length: ' + len(parsed_data).__str__())
        print('Unique products: ' + len(set(d['product_id'] for d in parsed_data)).__str__())

        Product.objects.filter(queryproduct__query=search_obj).delete()
        QueryProduct.objects.filter(query=search_obj).delete()

        batch = []
        for i, item in enumerate(parsed_data) :
            product, _ = Product.objects.update_or_create(
                product_id=item["product_id"],
                name= item["name"],
                price= item["price"],
                sale_price= item["sale_price"],
                rating= item["rating"],
                feedbacks= item["feedbacks"],
            )
            batch.append(product)

            if len(batch) >= 200:
                search_obj.products.add(*batch)
                batch.clear()
                search_obj.save()

        if batch:
            search_obj.products.add(*batch)

        search_obj.last_parsed = timezone.now()
        search_obj.save()

        return search_obj
