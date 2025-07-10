from typing import List, Dict, Any, Optional
from api.schemas import Product


def get_all_products_data(all_products_list: List[Product]) -> List[Product]:
    """
    Повертає повний список всіх продуктів.
    """
    return all_products_list


def get_product_by_name_data(product_name: str, products_by_name_map: Dict[str, Product]) -> Optional[Product]:
    """
    Знаходить продукт за назвою (регістронезалежний пошук).
    """
    return products_by_name_map.get(product_name.lower())


def get_product_field_data(product: Product, field_name: str) -> Optional[Any]:
    """
    Повертає значення конкретного поля продукту за його назвою.
    Пошук назви поля є регістронезалежним.
    """
    product_dict = product.model_dump()
    field_name_lower = field_name.lower()

    for key, value in product_dict.items():
        if key.lower() == field_name_lower:
            return {key: value}

    return None
