import re
from typing import List

import bs4
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Scraping.features import extract_float, get_driver, write_products_to_json


BASE_URL = "https://www.mcdonalds.com"
MENU_URL = BASE_URL + "/ua/uk-ua/eat/fullmenu.html"



def get_all_products_links() -> List:
    """
        Retrieves all product page URLs from the main McDonald's full menu page.

        Returns:
            List[str]: A list of full URLs to individual product pages.
    """

    response = requests.get(MENU_URL)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.content, "html.parser")

    # Find all product links on the menu page
    products_links = []
    anchors = soup.find_all("a", class_="cmp-category__item-link")

    for a in anchors:
        href = a.get("href")
        full_url = BASE_URL + href
        products_links.append(full_url)

    return products_links


def get_info_about_product_with_selenium(driver: webdriver.Chrome, url: str) -> dict:
    """
       Extract detailed product information including name, description,
       and nutritional values from the product page using Selenium.

       Args:
           driver (webdriver.Chrome): Selenium WebDriver instance.
           url (str): URL of the product page.

       Returns:
           dict: Dictionary containing product details and nutritional info.
    """

    driver.get(url)
    wait = WebDriverWait(driver, 10)

    product = {"url": url}

    try:
        # Wait and get product name and description elements
        name_el = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cmp-product-details-main__heading-title")))
        desc_el = driver.find_element(By.CLASS_NAME, "cmp-text")

        product["name"] = name_el.text.strip()
        product["description"] = desc_el.text.strip()

        # Expand nutrition facts accordion to load nutritional data
        button = driver.find_element(By.CLASS_NAME, "cmp-accordion__button")
        button.click()
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cmp-container")))

        # Gather nutritional data elements from two different blocks
        first_part = driver.find_elements(By.CLASS_NAME, "cmp-nutrition-summary__heading-primary-item")
        second_part = driver.find_elements(By.CLASS_NAME, "label-item")
        nutrition_items = first_part + second_part

        ukr_to_eng = {
            "калорійність": "calories",
            "жири": "fats",
            "вуглеводи": "carbs",
            "білки": "proteins",
            "ненасичені жири": "unsaturated_fats",
            "нжк:": "unsaturated_fats",
            "цукор:": "sugar",
            "сіль:": "salt",
            "порція:": "portion"
        }

        for item in nutrition_items:
            try:
                # Extract the nutrient name and value elements
                metric_el = item.find_element(By.CLASS_NAME, "metric")
                value_el = item.find_element(By.CLASS_NAME, "value")

                metric_text = metric_el.text.strip().lower()

                # Clean the metric text to match keys in ukr_to_eng
                metric_clean = re.split(r"\s*\(|\n", metric_text)[0].strip()

                value_text = value_el.text.strip()
                value_clean = extract_float(value_text)

                # Map Ukrainian nutrient name to English key and store value
                if metric_clean in ukr_to_eng:
                    key_eng = ukr_to_eng[metric_clean]
                    product[key_eng] = value_clean

            except Exception as e:
                print(f"Error reading nutrition item: {e}")
                continue

    except Exception as e:
        print(f"Error parsing product page {url}: {e}")

    return product


def get_all_products() -> None:
    """
        Main function to scrape all products from the McDonald's full menu page.
        Uses requests to get product URLs and Selenium to extract detailed data.
        Stores the final list of product dictionaries to a JSON file.
    """

    all_products_links = get_all_products_links()
    all_products_data = []

    with get_driver() as driver:

        for idx, product_url in enumerate(all_products_links, 1):
            print(f"[{idx}/{len(all_products_links)}] Parsing {product_url}")
            product_data = get_info_about_product_with_selenium(driver, product_url)

            if product_data:
                all_products_data.append(product_data)

    write_products_to_json(all_products_data)

if __name__ == "__main__":
    get_all_products()
