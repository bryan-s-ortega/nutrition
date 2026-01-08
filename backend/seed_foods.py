from sqlmodel import Session, select
from database import engine, create_db_and_tables
from models import FoodItem, FoodCategory


def seed_foods():
    create_db_and_tables()

    with Session(engine) as session:
        # Check if we already have foods
        existing = session.exec(select(FoodItem)).first()
        if existing:
            print(
                "Foods already seeded. Delete database.db to re-seed if schema changed."
            )
            return

        foods = [
            # Proteins
            FoodItem(
                name="Chicken Breast",
                calories=165,
                protein=31,
                carbs=0,
                fats=3,
                serving_size="100g",
                category=FoodCategory.PROTEIN,
            ),
            FoodItem(
                name="Ground Beef (90%)",
                calories=176,
                protein=20,
                carbs=0,
                fats=10,
                serving_size="100g",
                category=FoodCategory.PROTEIN,
            ),
            FoodItem(
                name="Salmon",
                calories=208,
                protein=20,
                carbs=0,
                fats=13,
                serving_size="100g",
                category=FoodCategory.PROTEIN,
            ),
            FoodItem(
                name="Tofu",
                calories=76,
                protein=8,
                carbs=2,
                fats=4,
                serving_size="100g",
                category=FoodCategory.PROTEIN,
            ),
            FoodItem(
                name="Eggs",
                calories=155,
                protein=13,
                carbs=1,
                fats=11,
                serving_size="100g",
                category=FoodCategory.PROTEIN,
            ),
            # Carbs
            FoodItem(
                name="White Rice (Cooked)",
                calories=130,
                protein=2,
                carbs=28,
                fats=0,
                serving_size="100g",
                category=FoodCategory.CARB,
            ),
            FoodItem(
                name="Sweet Potato",
                calories=86,
                protein=1,
                carbs=20,
                fats=0,
                serving_size="100g",
                category=FoodCategory.CARB,
            ),
            FoodItem(
                name="Oats",
                calories=389,
                protein=16,
                carbs=66,
                fats=6,
                serving_size="100g",
                category=FoodCategory.CARB,
            ),
            FoodItem(
                name="Pasta (Cooked)",
                calories=131,
                protein=5,
                carbs=25,
                fats=1,
                serving_size="100g",
                category=FoodCategory.CARB,
            ),
            FoodItem(
                name="Banana",
                calories=89,
                protein=1,
                carbs=22,
                fats=0,
                serving_size="100g",
                category=FoodCategory.FRUIT,
            ),
            # Fats
            FoodItem(
                name="Almonds",
                calories=579,
                protein=21,
                carbs=21,
                fats=49,
                serving_size="100g",
                category=FoodCategory.FAT,
            ),
            FoodItem(
                name="Avocado",
                calories=160,
                protein=2,
                carbs=8,
                fats=14,
                serving_size="100g",
                category=FoodCategory.FAT,
            ),
            # Veggies
            FoodItem(
                name="Broccoli",
                calories=55,
                protein=3,
                carbs=11,
                fats=0,
                serving_size="100g",
                category=FoodCategory.VEGETABLE,
            ),
            FoodItem(
                name="Spinach",
                calories=23,
                protein=2,
                carbs=3,
                fats=0,
                serving_size="100g",
                category=FoodCategory.VEGETABLE,
            ),
            # Dairy
            FoodItem(
                name="Greek Yogurt",
                calories=59,
                protein=10,
                carbs=3,
                fats=0,
                serving_size="100g",
                category=FoodCategory.DAIRY,
            ),
        ]

        for food in foods:
            session.add(food)

        session.commit()
        print("Seeded foods successfully!")


if __name__ == "__main__":
    seed_foods()
