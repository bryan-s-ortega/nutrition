import requests
from sqlmodel import Session, select
from models import MealPlanItem, FoodItem
from database import engine

# 1. Call API
url = "http://localhost:8000/onboarding"
data = {
    "age": 30,
    "weight": 80,
    "height": 180,
    "gender": "male",
    "goal": "muscle_gain",
    "activity_level": 1.5,
}
print(f"Calling {url}...")
try:
    response = requests.post(url, json=data)
    response.raise_for_status()
    plan = response.json()
    print(f"Plan Created: ID={plan['id']}, Calories={plan['calories']}")
except Exception as e:
    print(f"API Failed: {e}")
    exit(1)

# 2. Verify Items in DB
print("\n--- Meal Plan Items ---")
with Session(engine) as session:
    items = session.exec(
        select(MealPlanItem).where(MealPlanItem.meal_plan_id == plan["id"])
    ).all()
    for item in items:
        food = session.get(FoodItem, item.food_item_id)
        print(
            f"[{item.meal_type.value.upper()}] {food.name} ({food.category.value}): {item.amount:.2f} serving(s)"
        )
