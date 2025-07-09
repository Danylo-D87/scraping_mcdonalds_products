import json
from typing import List

import requests
import bs4


BASE_URL = "https://www.mcdonalds.com"
MENU_URL = BASE_URL + "/ua/uk-ua/eat/fullmenu.html"


def write_products_to_json(products: List) -> None:

    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)


def get_all_categories_links() -> List[str]:
    response = requests.get(MENU_URL)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.content, "html.parser")

    # Знайдемо всі посилання на categories
    categories_links = []
    anchors = soup.find_all("a", class_="category-link")

    for a in anchors:
        href = a.get("href")
        full_url = BASE_URL + href
        categories_links.append(full_url)

    return categories_links


def get_all_products_from_category(category_url: str) -> List:
    response = requests.get(category_url)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.content, "html.parser")

    # Знайдемо всі посилання на продукти
    products_links = []
    anchors = soup.find_all("a", class_="cmp-category__item-link")

    for a in anchors:
        href = a.get("href")
        full_url = BASE_URL + href
        products_links.append(full_url)

    return products_links


def get_info_about_product_with_selenium(url):
    pass


def get_single_product():
    pass


def get_all_products():
    categories_links = get_all_categories_links()

    all_products_links = []

    for category_link in categories_links:
        products_links = get_all_products_from_category(category_link)
        all_products_links.extend(products_links)

    write_products_to_json(all_products_links)


if __name__ == "__main__":
    get_all_products()
