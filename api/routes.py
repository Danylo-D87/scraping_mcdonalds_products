from fastapi import APIRouter, HTTPException, status, Depends, Request
from typing import List, Dict

from api.schemas import Product, ProductsListResponse
from api import crud


router = APIRouter()

# Dependencies for accessing global data
# These dependency functions access global variables from main.py
# via the app.state attribute (which we will add in main.py)
# This is a better way to pass data than using global directly in routes
def get_products_by_name_map(request: Request) -> Dict[str, Product]:
    return request.app.state.products_by_name


def get_all_products_list(request: Request) -> List[Product]:
    return request.app.state.all_products_list


@router.get("/", summary="Root endpoint")
def read_root():
    return {"message": "McDonald's Products API. Go to /docs for API documentation."}


@router.get("/all_products", response_model=ProductsListResponse, summary="Get all products with details")
def get_all_products_endpoint(
        all_products_list: List[Product] = Depends(get_all_products_list)
):
    """
    Returns a complete list of all available McDonald's products with their details and nutritional information.
    The data is loaded into application memory on startup for fast access.
    """
    return {"products": crud.get_all_products_data(all_products_list)}


@router.get(
    "/products/{product_name}",
    response_model=Product,
    summary="Get full product details by name"
)
def get_product_by_name(
        product_name: str,
        products_by_name_map: Dict[str, Product] = Depends(get_products_by_name_map)
):
    """
    Returns full information about a product by its name (case-insensitive search).
    """
    product = crud.get_product_by_name_data(product_name, products_by_name_map)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.get(
    "/products/{product_name}/field/{product_field}",
    summary="Get a specific field from a product by name and field name"
)
def get_product_field(
        product_name: str,
        product_field: str,
        products_by_name_map: Dict[str, Product] = Depends(get_products_by_name_map)
):
    """
    Returns the value of a specific product field by its name.
    Both the product name and the field name are searched case-insensitively.
    """
    product = crud.get_product_by_name_data(product_name, products_by_name_map)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    field_value = crud.get_product_field_data(product, product_field)

    if field_value is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Field '{product_field}' not found in product '{product_name}'")

    return field_value
