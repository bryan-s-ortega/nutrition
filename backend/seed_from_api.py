import asyncio
import sys
import os
from sqlmodel import Session, select

# Add project root to path
sys.path.append(os.getcwd())

from sqlmodel import SQLModel
from backend.database import engine, create_db_and_tables
from backend.models import FoodItem, FoodCategory, FoodSource, BrandedFood
from backend.services.usda_client import USDAClient
from backend.services.openfoodfacts_client import OpenFoodFactsClient

# Staple foods to seed
# Format: (Search Query, Category)
SEEDS = [
    ("Chicken Breast raw", FoodCategory.PROTEIN),
    ("Ground Beef 90% lean raw", FoodCategory.PROTEIN),
    ("Atlantic Salmon raw", FoodCategory.PROTEIN),
    ("Tofu raw", FoodCategory.PROTEIN),
    ("Egg raw", FoodCategory.PROTEIN),
    ("White Rice raw", FoodCategory.CARB),
    ("Sweet Potato raw", FoodCategory.CARB),
    ("Oats raw", FoodCategory.CARB),
    ("Banana raw", FoodCategory.FRUIT),
    ("Apple raw", FoodCategory.FRUIT),
    ("Almonds raw", FoodCategory.FAT),
    ("Avocado raw", FoodCategory.FAT),
    ("Broccoli raw", FoodCategory.VEGETABLE),
    ("Spinach raw", FoodCategory.VEGETABLE),
    ("Greek Yogurt plain", FoodCategory.DAIRY),
    ("Milk whole", FoodCategory.DAIRY),
]

# Open Food Facts Seeds (Branded/Specific)
OFF_SEEDS = [
    ("Nutella", FoodCategory.FAT),
    ("Oreo", FoodCategory.CARB),
    ("Coca Cola", FoodCategory.CARB),
    ("Doritos", FoodCategory.CARB),
    ("Protein Bar Quest", FoodCategory.PROTEIN),
]


async def seed_from_api():
    print("Re-creating database tables (Dropping old schema)...")
    # Drop all and recreate to ensure schema changes are applied
    # WARNING: This deletes all data!
    SQLModel.metadata.drop_all(engine)
    create_db_and_tables()

    client = USDAClient()
    off_client = OpenFoodFactsClient()
    if not client.api_key:
        print("ERROR: USDA_API_KEY not set. Cannot seed from API.")
        return

    async with asyncio.TaskGroup():
        # We could run these concurrently, but let's do sequential for rate limits ensuring
        # actually, let's just do sequential to be safe with USDA rate limits (1000/hr)
        pass

    with Session(engine) as session:
        print(f"Starting seed of {len(SEEDS)} items...")

        for query, category in SEEDS:
            print(f"Searching for '{query}'...")
            try:
                # Search for the food
                results = await client.search_foods(query, page_size=1)

                if not results:
                    print(f"  No results found for '{query}'")
                    continue

                # Parse the best match
                item_data = client.parse_food_item(results[0])

                # Check for duplicate by name (exact match might fail, but let's try)
                # Or check by external_id if we want to be strict, but we are just seeding names
                # Let's check by matching name roughly or just trust the user wants these specific ones

                # Check if this exact FDC ID exists?
                existing = session.exec(
                    select(FoodItem).where(
                        FoodItem.external_id == item_data["external_id"]
                    )
                ).first()
                if existing:
                    print(f"  Skipping '{item_data['name']}' (already exists)")
                    continue

                if not item_data["calories"]:
                    print(f"  Skipping '{item_data['name']}' (missing calorie data)")
                    continue

                # Create FoodItem
                food = FoodItem(
                    name=item_data["name"],
                    calories=int(item_data["calories"]),
                    protein=int(item_data["protein"]),
                    carbs=int(item_data["carbs"]),
                    fats=int(item_data["fats"]),
                    serving_size=item_data["serving_size"],
                    category=category,
                    source=FoodSource.USDA,
                    external_id=item_data["external_id"],
                    brand=item_data["brand"],
                )

                session.add(food)
                print(f"  Added: {food.name} ({food.calories} kcal)")

            except Exception as e:
                print(f"  Error processing '{query}': {e}")

        print(f"Starting OFF seed of {len(OFF_SEEDS)} items...")
        for query, category in OFF_SEEDS:
            print(f"Searching OFF for '{query}'...")
            try:
                # Search OFF
                results = await off_client.search_products(query, page_size=1)

                if not results:
                    print(f"  No results found for '{query}'")
                    continue

                item_data = off_client.parse_product(results[0])

                # Check duplication in BrandedFood
                existing = session.exec(
                    select(BrandedFood).where(
                        BrandedFood.barcode == item_data["barcode"]
                    )
                ).first()
                if existing:
                    print(f"  Skipping '{item_data['name']}' (already exists)")
                    continue

                # Create BrandedFood
                food = BrandedFood(
                    name=item_data["name"],
                    brand=item_data["brand"],
                    barcode=item_data["barcode"],
                    calories=int(float(item_data["calories"] or 0)),
                    protein=int(float(item_data["protein"] or 0)),
                    carbs=int(float(item_data["carbs"] or 0)),
                    fats=int(float(item_data["fats"] or 0)),
                    serving_size=item_data["serving_size"] or "100g",
                    external_id=item_data["external_id"],
                    # image_url could be added to client parsing if needed
                )
                session.add(food)
                print(f"  Added to BrandedFood: {food.name}")
            except Exception as e:
                print(f"  Error processing OFF '{query}': {e}")

        session.commit()
        print("Seeding complete!")


if __name__ == "__main__":
    asyncio.run(seed_from_api())
