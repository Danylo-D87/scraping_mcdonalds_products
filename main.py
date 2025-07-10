from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
import json
from typing import List, Dict, Any

from api.settings import get_settings
from api.schemas import Product, ProductsListResponse


settings = get_settings()

app_products_by_name: Dict[str, Product] = {}
app_all_products_list: List[Product] = []


@asynccontextmanager
async def lifespan():
    """
    Context manager for handling application lifecycle events (startup/shutdown).
    Loads product data from a JSON file into application memory on startup.
    """
    global app_products_by_name, app_all_products_list

    try:
        with open(settings.products_file_path, "r", encoding="utf-8") as f:
            raw_products_data: List[Dict[str, Any]] = json.load(f)

            all_products: List[Product] = []
            products_map: Dict[str, Product] = {}

            for product_data in raw_products_data:
                try:
                    product = Product(**product_data)
                    all_products.append(product)
                    products_map[product.name.lower()] = product
                except Exception as e:
                    continue

            app_products_by_name = products_map
            app_all_products_list = all_products

    except FileNotFoundError:
        app_products_by_name = {}
        app_all_products_list = []
    except json.JSONDecodeError:
        app_products_by_name = {}
        app_all_products_list = []
    except Exception as e:
        app_products_by_name = {}
        app_all_products_list = []

    yield

    print("ℹ️ Додаток FastAPI завершує роботу.")


app = FastAPI(
    title="McDonald's Products API",
    description="API for retrieving information about McDonald's products and their nutritional values.",
    version="1.0.0",
    lifespan=lifespan
)


# Base endpoints

@app.get("/", summary="Root endpoint")
def read_root():
    return {
        "message": "McDonald's Products API. Go to /docs for API documentation."
    }


# Оновлений ендпоінт для отримання всіх продуктів
@app.get("/all_products", response_model=ProductsListResponse, summary="Get all products with details")
def get_all_products_endpoint():
    """
    Returns a complete list of all available McDonald's products with their details and nutritional information.
    The data is loaded into application memory on startup for fast access.
    """

    return {"products": app_all_products_list}


@app.get(
    "/products/{product_name}",
    response_model=Product,
    summary="Get full product details by name"
)
def get_product_by_name(product_name: str):
    """
    Returns full information about a product by its name (case-insensitive search).
    """

    product = app_products_by_name.get(product_name.lower())

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@app.get(
    "/products/{product_name}/field/{product_field}",
    summary="Get a specific field from a product by name and field name"
)
def get_product_field(product_name: str, product_field: str):
    """
    Returns the value of a specific product field by its name.
    Both product name and field name searches are case-insensitive.
    """

    product = app_products_by_name.get(product_name.lower())
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    product_dict = product.model_dump()

    product_field_lower = product_field.lower()
    for key, value in product_dict.items():
        if key.lower() == product_field_lower:
            return {key: value}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Field '{product_field}' not found in product '{product_name}'"
    )
