from typing import Optional, List

from pydantic import BaseModel, Field


class Product(BaseModel):
    url: Optional[str] = None
    name: str = Field(..., description="The name of the product")
    description: Optional[str] = None
    calories: Optional[float] = None
    fats: Optional[float] = None
    carbs: Optional[float] = None
    proteins: Optional[float] = None
    unsaturated_fats: Optional[float] = None
    sugar: Optional[float] = None
    salt: Optional[float] = None
    portion: Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Big Mac",
                "description": "The iconic Big Mac.",
                "calories": 550.0,
                "fats": 29.0,
                "carbs": 46.0,
                "proteins": 27.0,
                "url": "https://www.mcdonalds.com/ua/uk-ua/product/bigmac.html"
            }
        }

class ProductsListResponse(BaseModel):
    products: List[Product]
