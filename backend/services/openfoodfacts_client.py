import httpx
from typing import Optional, List, Dict, Any


class OpenFoodFactsClient:
    # Using the US world endpoint, but could be customizable
    BASE_URL = "https://us.openfoodfacts.org/api/v2"

    async def search_products(
        self, query: str, page_size: int = 10
    ) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            try:
                # OFF search API is a bit complex, utilizing the search endpoint
                # https://us.openfoodfacts.org/cgi/search.pl?search_terms=coke&search_simple=1&action=process&json=1
                response = await client.get(
                    "https://us.openfoodfacts.org/cgi/search.pl",
                    params={
                        "search_terms": query,
                        "search_simple": 1,
                        "action": "process",
                        "json": 1,
                        "page_size": page_size,
                        "fields": "product_name,brands,nutriments,image_url,code,id,_keywords,nutriscore_grade",
                    },
                )
                response.raise_for_status()
                data = response.json()
                return data.get("products", [])
            except httpx.HTTPError as e:
                print(f"OFF API Error: {e}")
                return []

    async def get_product_by_barcode(self, barcode: str) -> Optional[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/product/{barcode}",
                    params={
                        "fields": "product_name,brands,nutriments,image_url,nutriscore_grade,ingredients_text"
                    },
                )
                response.raise_for_status()
                data = response.json()
                if data.get("status") == 1:
                    return data.get("product")
                return None
            except httpx.HTTPError as e:
                print(f"OFF API Error: {e}")
                return None

    @staticmethod
    def parse_product(item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses a raw Open Food Facts product into a simplified dictionary.
        """
        nutriments = item.get("nutriments", {})

        # OFF usually provides values per 100g
        return {
            "name": item.get("product_name", "Unknown"),
            "brand": item.get("brands"),
            "calories": nutriments.get("energy-kcal_100g", 0),
            "protein": nutriments.get("proteins_100g", 0),
            "carbs": nutriments.get("carbohydrates_100g", 0),
            "fats": nutriments.get("fat_100g", 0),
            "serving_size": item.get("serving_size", "100g"),
            "external_id": item.get("code", ""),
            "barcode": item.get("code", ""),
        }
