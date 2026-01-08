import requests
from typing import List
from models import FoodItem, FoodSource


def search_off(query: str) -> List[FoodItem]:
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": query,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 5,
    }

    headers = {"User-Agent": "NutritionApp/1.0 (Integration Test) - python-requests"}

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        results = []
        for product in data.get("products", []):
            nutriments = product.get("nutriments", {})

            # OFF often has keys like 'energy-kcal_100g'
            calories = nutriments.get("energy-kcal_100g", 0) or nutriments.get(
                "energy-kcal", 0
            )
            protein = nutriments.get("proteins_100g", 0) or nutriments.get(
                "proteins", 0
            )
            carbs = nutriments.get("carbohydrates_100g", 0) or nutriments.get(
                "carbohydrates", 0
            )
            fats = nutriments.get("fat_100g", 0) or nutriments.get("fat", 0)

            item = FoodItem(
                name=product.get("product_name", "Unknown Product"),
                calories=int(float(calories or 0)),
                protein=int(float(protein or 0)),
                carbs=int(float(carbs or 0)),
                fats=int(float(fats or 0)),
                serving_size=product.get("serving_size", "100g"),
                source=FoodSource.OFF,
                external_id=str(product.get("_id", "")),
                brand=product.get("brands", ""),
                barcode=str(product.get("code", "")),
            )
            results.append(item)

        return results

    except Exception as e:
        print(f"Open Food Facts API Error: {e}")
        return []
