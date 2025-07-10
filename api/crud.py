from typing import List, Dict, Any, Optional
from api.schemas import Product


def get_all_products_data(all_products_list: List[Product]) -> List[Product]:
    """
    Returns the complete list of all products.
    """
    return all_products_list


def get_product_by_name_data(product_name: str, products_by_name_map: Dict[str, Product]) -> Optional[Product]:
    """
    Finds a product by its name (case-insensitive search).
    """
    return products_by_name_map.get(product_name.lower())


def get_product_field_data(product: Product, field_name: str) -> Optional[Any]:
    """
    Returns the value of a specific product field by its name.
    The field name search is case-insensitive.
    """
    product_dict = product.model_dump()
    field_name_lower = field_name.lower()

    for key, value in product_dict.items():
        if key.lower() == field_name_lower:
            return {key: value}

    return None
