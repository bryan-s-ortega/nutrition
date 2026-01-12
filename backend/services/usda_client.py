import os
import httpx
from typing import Optional, List, Dict, Any


class USDAClient:
    BASE_URL = "https://api.nal.usda.gov/fdc/v1"

    def __init__(self):
        self.api_key = os.getenv("USDA_API_KEY")
        if not self.api_key:
            # We don't raise error here to allow app to start, but methods will fail
            print("WARNING: USDA_API_KEY not set")

    async def search_foods(
        self, query: str, page_size: int = 10
    ) -> List[Dict[str, Any]]:
        if not self.api_key:
            return []

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/foods/search",
                    params={
                        "api_key": self.api_key,
                        "query": query,
                        "pageSize": page_size,
                        # Prioritize foundation and legacy foods for generic searches
                        "dataType": ["Foundation", "SR Legacy"],
                    },
                )
                response.raise_for_status()
                data = response.json()
                return data.get("foods", [])
            except httpx.HTTPError as e:
                print(f"USDA API Error: {e}")
                return []

    async def get_food_details(self, fdc_id: int) -> Optional[Dict[str, Any]]:
        if not self.api_key:
            return None

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/food/{fdc_id}", params={"api_key": self.api_key}
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"USDA API Error: {e}")
                return None

    @staticmethod
    def parse_food_item(item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses a raw USDA food item into a simplified dictionary with:
        name, brand, calories, protein, carbs, fats, serving_size, external_id
        """
        nutrients_by_id = {
            n["nutrientId"]: n["value"] for n in item.get("foodNutrients", [])
        }

        # USDA Nutrient IDs:
        # Energy (kcal): 1008
        # Protein: 1003
        # Total lipid (fat): 1004
        # Carbohydrate, by difference: 1005

        return {
            "name": item.get("description"),
            "brand": item.get("brandOwner"),
            "calories": nutrients_by_id.get(1008, 0),
            "protein": nutrients_by_id.get(1003, 0),
            "carbs": nutrients_by_id.get(1005, 0),
            "fats": nutrients_by_id.get(1004, 0),
            "serving_size": f"{item.get('servingSize')} {item.get('servingSizeUnit')}"
            if item.get("servingSize")
            else "100g",
            "external_id": str(item.get("fdcId")),
        }
