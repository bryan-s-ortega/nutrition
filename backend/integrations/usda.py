import requests
from typing import List
from models import FoodItem, FoodSource


def search_usda(query: str, api_key: str) -> List[FoodItem]:
    if not api_key:
        print("Warning: No USDA API Key provided.")
        return []

    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "query": query,
        "api_key": api_key,
        "dataType": ["Branded", "Foundation"],
        "pageSize": 5,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        results = []
        for food in data.get("foods", []):
            # Extract nutrients
            nutrients = {
                n["nutrientName"]: n["value"] for n in food.get("foodNutrients", [])
            }

            # Simple fuzzy matching for keys
            # Energy (Atwater General Factors) or Energy
            calories = nutrients.get("Energy", 0)
            protein = nutrients.get("Protein", 0)
            carbs = nutrients.get("Carbohydrate, by difference", 0)
            fats = nutrients.get("Total lipid (fat)", 0)

            item = FoodItem(
                name=food.get("description"),
                calories=int(calories),
                protein=int(protein),
                carbs=int(carbs),
                fats=int(fats),
                serving_size=food.get("servingSize", "100g") or "100g",
                source=FoodSource.USDA,
                external_id=str(food.get("fdcId")),
                brand=food.get("brandOwner"),
                barcode=food.get("gtinUpc"),
            )
            results.append(item)

        return results

    except Exception as e:
        print(f"USDA API Error: {e}")
        return []
