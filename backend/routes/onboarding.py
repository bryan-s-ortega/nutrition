from fastapi import APIRouter, Depends
from sqlmodel import Session

# Support both `backend.routes.onboarding` and `routes.onboarding` import styles.
try:
    from ..database import get_session
    from ..models import User, MealPlan, Goal, Gender
except ImportError:  # pragma: no cover
    from database import get_session
    from models import User, MealPlan, Goal, Gender

router = APIRouter()

@router.post("/onboarding", response_model=MealPlan)
def onboarding(user: User, session: Session = Depends(get_session)):
    # 1. Save User
    session.add(user)
    session.commit()
    session.refresh(user)

    # 2. Calculate BMR (Mifflin-St Jeor)
    if user.gender == Gender.MALE:
        bmr = 10 * user.weight + 6.25 * user.height - 5 * user.age + 5
    else:
        bmr = 10 * user.weight + 6.25 * user.height - 5 * user.age - 161

    # 3. Calculate TDEE
    tdee = bmr * user.activity_level

    # 4. Adjust for Goal
    if user.goal == Goal.WEIGHT_LOSS:
        target_calories = tdee - 500
    elif user.goal == Goal.MUSCLE_GAIN:
        target_calories = tdee + 300
    else:
        target_calories = tdee

    # 5. Calculate Macros
    # Protein: 2g per kg (approx)
    protein_grams = int(user.weight * 2)
    protein_cals = protein_grams * 4

    # Fats: 0.8g per kg
    fats_grams = int(user.weight * 0.8)
    fats_cals = fats_grams * 9

    # Carbs: Remainder
    remaining_cals = target_calories - protein_cals - fats_cals
    carbs_grams = int(remaining_cals / 4)

    # 6. Create Meal Plan (Targets)
    meal_plan = MealPlan(
        user_id=user.id,
        calories=int(target_calories),
        protein=protein_grams,
        carbs=carbs_grams,
        fats=fats_grams,
        name=f"Plan for {user.goal.value}"
    )

    session.add(meal_plan)
    session.commit()
    session.refresh(meal_plan)

    # 7. Generate Meal Plan Items
    from meal_generator import generate_meal_plan
    generate_meal_plan(meal_plan, session)
    
    # Refresh to load items if we want to return them (though response model currently uses MealPlan which might not show items unless updated)
    session.refresh(meal_plan)

    return meal_plan
