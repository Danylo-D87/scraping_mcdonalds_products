from contextlib import asynccontextmanager
from fastapi import FastAPI
import json
from typing import List, Dict, Any

from api.settings import get_settings
from api.schemas import Product
from api import routes


settings = get_settings()

app_products_by_name: Dict[str, Product] = {}
app_all_products_list: List[Product] = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for handling application lifecycle events (startup/shutdown).
    Loads product data from a JSON file into application memory on startup.
    """
    global app_products_by_name, app_all_products_list

    print(f"Attempt to load product data from: {settings.products_file_path}")
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
                    print(f"Data validation error for the product '{product_data.get('name', 'N/A')}': {e}")
                    continue

            app_products_by_name = products_map
            app_all_products_list = all_products
            print(f"Product data successfully loaded from '{settings.products_file_path}'. Loaded {len(app_all_products_list)} products.")

    except FileNotFoundError:
        print(f"Error: Product file '{settings.products_file_path}' not found at startup. Please ensure that scraping was run and the file exists.")
        app_products_by_name = {}
        app_all_products_list = []
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from file '{settings.products_file_path}'. Please check the file format.")
        app_products_by_name = {}
        app_all_products_list = []
    except Exception as e:
        print(f"Unexpected error occurred while loading product data: {e}")
        app_products_by_name = {}
        app_all_products_list = []

    app.state.products_by_name = app_products_by_name
    app.state.all_products_list = app_all_products_list

    yield

    print("FastAPI application is shutting down.")


app = FastAPI(
    title="McDonald's Products API",
    description="API for retrieving information about McDonald's products and their nutritional values.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(routes.router)
