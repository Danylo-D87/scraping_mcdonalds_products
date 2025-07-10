import json
import re
from contextlib import contextmanager
from typing import List

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from api.settings import get_settings


@contextmanager
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        yield driver
    finally:
        driver.quit()


def write_products_to_json(products: List) -> None:

    settings = get_settings()
    with open(settings.products_file_path, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)


def extract_float(text: str) -> float | None:
    if not text:
        return None
    first_line = text.split('\n')[0].strip()
    match = re.search(r"[\d.,]+", first_line)
    return float(match.group(0).replace(',', '.')) if match else None
