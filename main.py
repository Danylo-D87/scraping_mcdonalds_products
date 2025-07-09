from fastapi import FastAPI, HTTPException
import json

from Scraping.scraping import get_all_products

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "McDonald's Products API"}


@app.get("/all_products", summary="Get all products")
def get_products():
    """ Returns the list of all products saved in products.json. """

    try:
        with open("Scraping/products.json", "r", encoding="utf-8") as f:
            products = json.load(f)
        return products
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Products not found.")


@app.get(
    "/products/{product_name}/{product_field}",
    summary="Get specific field from a product"
)
def get_product(product_name: str):
    """
    Return the full information about a product by its name.
    Case-insensitive match.
    """
    with open("Scraping/products.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    for product in products:
        if product_name.lower() == product.get("name", "").lower():
            return product
    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/products/{product_name}/{product_field}")
def get_product_field(product_name: str, product_field: str):
    """
    Return a specific field from a product.
    Case-insensitive name and field match.
    """

    with open("Scraping/products.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    for product in products:
        if product_name.lower() == product.get("name", "").lower():
            # return only the requested field if it exists
            for key, value in product.items():
                if key.lower() == product_field.lower():
                    return {key: value}
            raise HTTPException(status_code=404, detail="Field not found in product")
    raise HTTPException(status_code=404, detail="Product not found")
