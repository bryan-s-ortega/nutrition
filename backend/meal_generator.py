from sqlmodel import Session, select
from models import MealPlan, MealPlanItem, FoodItem, MealType, FoodCategory
import random


def get_food_by_category(session: Session, category: FoodCategory) -> FoodItem:
    """Helper to get a random food item by category."""
    foods = session.exec(select(FoodItem).where(FoodItem.category == category)).all()
    if not foods:
        return None
    return random.choice(foods)


def add_meal_item(
    session: Session,
    plan_id: int,
    food: FoodItem,
    meal_type: MealType,
    target_macro_grams: int,
    macro_type: str,  # 'protein', 'carbs', or 'fats'
):
    """
    Adds a food item to the plan, scaling amount to meet a specific macro target.
    """
    if not food:
        return

    # Calculate amount. food.protein is per 100g (serving_size is string, assume base values are per serving)
    # Actually models says serving_size is "100g", and values are integers.
    # Let's assume the values in DB are for 1 serving.

    food_macro_value = getattr(food, macro_type)

    if food_macro_value <= 0:
        amount = 1.0  # Fallback
    else:
        # We want to get 'target_macro_grams' from this food.
        # amount = target / food_value
        amount = target_macro_grams / food_macro_value

    item = MealPlanItem(
        meal_plan_id=plan_id,
        food_item_id=food.id,
        amount=round(amount, 2),
        meal_type=meal_type,
    )
    session.add(item)


def generate_meal_plan(target_plan: MealPlan, session: Session):
    """
    Generates meal plan items dynamically to meet the target calories and macros.
    V2: Dynamic Selection based on Categories.
    """

    # Targets
    daily_protein = target_plan.protein
    daily_carbs = target_plan.carbs
    daily_fats = target_plan.fats

    # Distribution Strategy (Approximate)
    # Breakfast: 30%
    # Lunch: 35%
    # Dinner: 25%
    # Snack: 10%

    # --- Breakfast (Protein + Carb) ---
    p_src = get_food_by_category(session, FoodCategory.PROTEIN)  # e.g. Eggs
    c_src = get_food_by_category(session, FoodCategory.CARB)  # e.g. Oats

    # Target: 30% of daily protein
    add_meal_item(
        session,
        target_plan.id,
        p_src,
        MealType.BREAKFAST,
        daily_protein * 0.3,
        "protein",
    )
    # Target: 30% of daily carbs
    add_meal_item(
        session, target_plan.id, c_src, MealType.BREAKFAST, daily_carbs * 0.3, "carbs"
    )

    # --- Lunch (Protein + Carb + Veggie + Fat) ---
    p_src = get_food_by_category(session, FoodCategory.PROTEIN)
    c_src = get_food_by_category(session, FoodCategory.CARB)
    v_src = get_food_by_category(session, FoodCategory.VEGETABLE)
    f_src = get_food_by_category(session, FoodCategory.FAT)

    add_meal_item(
        session, target_plan.id, p_src, MealType.LUNCH, daily_protein * 0.35, "protein"
    )
    add_meal_item(
        session, target_plan.id, c_src, MealType.LUNCH, daily_carbs * 0.35, "carbs"
    )
    add_meal_item(
        session, target_plan.id, v_src, MealType.LUNCH, 10, "carbs"
    )  # Veggies just for health, small carb contrib
    add_meal_item(
        session, target_plan.id, f_src, MealType.LUNCH, daily_fats * 0.4, "fats"
    )

    # --- Dinner (Protein + Carb + Veggie + Fat) ---
    p_src = get_food_by_category(session, FoodCategory.PROTEIN)
    c_src = get_food_by_category(session, FoodCategory.CARB)
    v_src = get_food_by_category(session, FoodCategory.VEGETABLE)
    f_src = get_food_by_category(session, FoodCategory.FAT)

    add_meal_item(
        session, target_plan.id, p_src, MealType.DINNER, daily_protein * 0.25, "protein"
    )
    add_meal_item(
        session, target_plan.id, c_src, MealType.DINNER, daily_carbs * 0.25, "carbs"
    )
    add_meal_item(session, target_plan.id, v_src, MealType.DINNER, 10, "carbs")
    add_meal_item(
        session, target_plan.id, f_src, MealType.DINNER, daily_fats * 0.4, "fats"
    )

    # --- Snack (Fruit or Dairy) ---
    s_src = get_food_by_category(session, FoodCategory.FRUIT) or get_food_by_category(
        session, FoodCategory.DAIRY
    )
    add_meal_item(
        session, target_plan.id, s_src, MealType.SNACK, daily_carbs * 0.1, "carbs"
    )

    session.commit()
