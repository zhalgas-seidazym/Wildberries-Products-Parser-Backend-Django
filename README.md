# 🧰 Wildberries Products Parser — Backend (Django REST API)

This project implements a backend service for parsing Wildberries product data and providing access via a RESTful API.

---

## 🚀 Features

- Parse Wildberries products using custom query terms
- Store and associate products with search queries in the database
- Django REST API with filtering, pagination, and sorting
- Swagger documentation with drf-spectacular
- Filtering by price, sale price, rating, and number of reviews

---

## 💪 Tech Stack

- Python 3
- Django + Django REST Framework
- drf-spectacular (OpenAPI docs)
- django-filter
- SQLite (default)

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/zhalgas-seidazym/Wildberries-Products-Parser-Backend-Django.git
cd Wildberries-Products-Parser-Backend-Django
```

### 2. Create virtual environment & install dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. (Optional) Create superuser
```bash
python manage.py createsuperuser
```

### 5. Run development server
```bash
python manage.py runserver
```

---

## 🔗 API Endpoints

### Product List (with parsing)
```
GET /api/products/?query=<your_search_text>
```

#### Query Parameters:
- `min_price`, `max_price`
- `min_sale_price`, `max_sale_price`
- `min_rating`, `min_reviews`
- `page`, `page_size`

### Swagger/OpenAPI Docs
- Swagger UI: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- ReDoc: [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)
- OpenAPI JSON: `/api/schema/`

---

## 📁 Project Structure

```
products/
├── filters.py         # API filters
├── models.py          # Product, SearchQuery, QueryProduct
├── serializers.py     # DRF serializers
├── services.py        # Parsing & save logic
└── views.py           # ProductListView with filtering & pagination
```

---

## ✅ How It Works

1. User sends request to `/api/products/?query=shoes`
2. `ProductService.refresh_search_query()`:
   - Parses products from Wildberries
   - Saves or updates them in DB
   - Links products with the current search query
3. Filtered & paginated response is returned
