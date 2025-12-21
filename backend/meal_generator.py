from sqlmodel import Session, select
from models import MealPlan, MealPlanItem, FoodItem, MealType

def generate_meal_plan(target_plan: MealPlan, session: Session):
    """
    Generates meal plan items to meet the target calories and macros.
    This is a V1 implementation using a simple template.
    """
    
    # 1. Fetch available foods
    foods = session.exec(select(FoodItem)).all()
    if not foods:
        print("No foods found in database.")
        return

    food_map = {f.name: f for f in foods}
    
    # Simple template:
    # Breakfast: Oats + Eggs
    # Lunch: Chicken + Rice + Broccoli
    # Dinner: Chicken + Rice + Broccoli
    # Snack: Greek Yogurt + Almonds (if needed) works as filler
    
    # Let's try to fit roughly.
    # Currently just hardcoding some sensible defaults scaled by calories?
    # Or just adding fixed items for now to prove structure works.
    
    # Let's just create a fixed menu for everyone for V1 to ensure DB works.
    
    items = []
    
    # Breakfast
    if "Oats" in food_map:
        items.append(MealPlanItem(meal_plan_id=target_plan.id, food_item_id=food_map["Oats"].id, amount=0.5, meal_type=MealType.BREAKFAST)) # 50g
    if "Eggs" in food_map:
        items.append(MealPlanItem(meal_plan_id=target_plan.id, food_item_id=food_map["Eggs"].id, amount=2.0, meal_type=MealType.BREAKFAST)) # 2 eggs (approx)

    # Lunch
    if "Chicken Breast" in food_map:
         items.append(MealPlanItem(meal_plan_id=target_plan.id, food_item_id=food_map["Chicken Breast"].id, amount=1.5, meal_type=MealType.LUNCH))
    if "White Rice (Cooked)" in food_map:
         items.append(MealPlanItem(meal_plan_id=target_plan.id, food_item_id=food_map["White Rice (Cooked)"].id, amount=1.5, meal_type=MealType.LUNCH))
    if "Broccoli" in food_map:
         items.append(MealPlanItem(meal_plan_id=target_plan.id, food_item_id=food_map["Broccoli"].id, amount=1.0, meal_type=MealType.LUNCH))

    # Dinner (Same as lunch for simplicity)
    if "Chicken Breast" in food_map:
         items.append(MealPlanItem(meal_plan_id=target_plan.id, food_item_id=food_map["Chicken Breast"].id, amount=1.5, meal_type=MealType.DINNER))
    if "White Rice (Cooked)" in food_map:
         items.append(MealPlanItem(meal_plan_id=target_plan.id, food_item_id=food_map["White Rice (Cooked)"].id, amount=1.5, meal_type=MealType.DINNER))
    
    # Snack
    if "Greek Yogurt" in food_map:
         items.append(MealPlanItem(meal_plan_id=target_plan.id, food_item_id=food_map["Greek Yogurt"].id, amount=1.5, meal_type=MealType.SNACK))

    for item in items:
        # Check if we have an ID for the plan (it should be saved)
        if target_plan.id:
            item.meal_plan_id = target_plan.id
        session.add(item)
    
    session.commit()
