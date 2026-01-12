from fastapi import APIRouter, Query
from typing import List, Optional
from pydantic import BaseModel
from services.usda_client import USDAClient
from services.openfoodfacts_client import OpenFoodFactsClient

router = APIRouter(prefix="/foods", tags=["foods"])


class FoodSearchResult(BaseModel):
    name: str
    brand: Optional[str] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fats: Optional[float] = None
    serving_size: Optional[str] = None
    source: str  # "usda" or "off"
    external_id: str


@router.get("/search", response_model=List[FoodSearchResult])
async def search_foods(
    q: str = Query(..., min_length=2),
    source: str = Query("usda", enum=["usda", "off"]),
    limit: int = 10,
):
    results = []

    if source == "usda":
        client = USDAClient()
        items = await client.search_foods(q, page_size=limit)
        for item in items:
            # USDA data structure parsing
            # Nutrients are in a list 'foodNutrients'
            # nutrients = {
            #    n["nutrientName"]: n["value"] for n in item.get("foodNutrients", [])
            # }

            # Map common nutrient names (USDA names vary, this is a simplified mapping)
            # In a real app we'd map NDB numbers.
            # Protein: 203, Fat: 204, Carbs: 205, Energy (kcal): 208

            nutrients_by_id = {
                n["nutrientId"]: n["value"] for n in item.get("foodNutrients", [])
            }

            results.append(
                FoodSearchResult(
                    name=item.get("description"),
                    brand=item.get("brandOwner"),
                    calories=nutrients_by_id.get(1008),  # Energy
                    protein=nutrients_by_id.get(1003),  # Protein
                    carbs=nutrients_by_id.get(1005),  # Carbs
                    fats=nutrients_by_id.get(1004),  # Total lipid (fat)
                    serving_size=f"{item.get('servingSize')} {item.get('servingSizeUnit')}"
                    if item.get("servingSize")
                    else "100g",
                    source="usda",
                    external_id=str(item.get("fdcId")),
                )
            )

    elif source == "off":
        client = OpenFoodFactsClient()
        items = await client.search_products(q, page_size=limit)
        for item in items:
            nutriments = item.get("nutriments", {})
            results.append(
                FoodSearchResult(
                    name=item.get("product_name", "Unknown"),
                    brand=item.get("brands"),
                    calories=nutriments.get("energy-kcal_100g"),
                    protein=nutriments.get("proteins_100g"),
                    carbs=nutriments.get("carbohydrates_100g"),
                    fats=nutriments.get("fat_100g"),
                    serving_size=item.get("serving_size", "100g"),
                    source="off",
                    external_id=item.get("code", ""),
                )
            )

    return results
