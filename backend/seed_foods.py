from sqlmodel import Session, select
from database import engine, create_db_and_tables
from models import FoodItem


def seed_foods():
    create_db_and_tables()

    with Session(engine) as session:
        # Check if we already have foods
        existing = session.exec(select(FoodItem)).first()
        if existing:
            print("Foods already seeded.")
            return

        foods = [
            FoodItem(
                name="Chicken Breast",
                calories=165,
                protein=31,
                carbs=0,
                fats=3,
                serving_size="100g",
            ),
            FoodItem(
                name="White Rice (Cooked)",
                calories=130,
                protein=2,
                carbs=28,
                fats=0,
                serving_size="100g",
            ),
            FoodItem(
                name="Broccoli",
                calories=55,
                protein=3,
                carbs=11,
                fats=0,
                serving_size="100g",
            ),
            FoodItem(
                name="Oats",
                calories=389,
                protein=16,
                carbs=66,
                fats=6,
                serving_size="100g",
            ),
            FoodItem(
                name="Eggs",
                calories=155,
                protein=13,
                carbs=1,
                fats=11,
                serving_size="100g",
            ),
            FoodItem(
                name="Banana",
                calories=89,
                protein=1,
                carbs=22,
                fats=0,
                serving_size="100g",
            ),
            FoodItem(
                name="Almonds",
                calories=579,
                protein=21,
                carbs=21,
                fats=49,
                serving_size="100g",
            ),
            FoodItem(
                name="Greek Yogurt",
                calories=59,
                protein=10,
                carbs=3,
                fats=0,
                serving_size="100g",
            ),
        ]

        for food in foods:
            session.add(food)

        session.commit()
        print("Seeded foods successfully!")


if __name__ == "__main__":
    seed_foods()
