# McDonald's Products Scraper & API

This project scrapes McDonald's Ukraine menu products from https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html, extracts detailed product information including nutritional facts, and provides a simple FastAPI-based REST API to query the data.

---

## Features

- Scrapes all McDonald's menu products and their nutritional information.
- Saves product data as JSON.
- Provides FastAPI endpoints to get:
  - All products list
  - Specific product by name (case-insensitive)
  - Specific nutritional or descriptive field for a given product

---

## Setup & Installation

### Requirements

- requests
-   beautifulsoup4
- selenium
- fastapi
- uvicorn
---
## Usage

### 1. Scrape product data

Run the scraping script in:

```bash
Scraping/scraping.py
```

###  2. Start the API server
Run FastAPI with:

```bash
uvicorn main:app --reload
```
The API will be available at http://127.0.0.1:8000.

## API Endpoints

### GET `/`
Returns a simple welcome message.

**Response example:**
```json
{
  "message": "McDonald's Products API"
}
```
---
### GET `/all_product`
Returns a list of all available products.

---
### GET   `/products/{product_name}`

Response example:
```json
{
  "url": "https://www.mcdonalds.com/ua/uk-ua/eat/big-mac.html",
  "name": "Big Mac",
  "description": "Two 100% pure beef patties...",
  "calories": 550,
  "fats": 30,
  "carbs": 45,
  "proteins": 25
}
```
---

### GET   `/products/{product_name}/field/{product_field}`

Returns a specific field value from a product by product name and field (both case-insensitive).

Response example:
```json
{
  "calories": 550
}
```


#   Notes
- Nutritional fields currently supported include: calories, fats, carbs, proteins, unsaturated_fats, sugar, salt, portion.
- Make sure ChromeDriver matches your installed Chrome version.

- Selenium is used to extract detailed nutritional info from dynamic content.
