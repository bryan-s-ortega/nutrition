from sqlmodel import Session, select
from database import engine
from models import MealPlanItem, MealPlan

def verify_db():
    with Session(engine) as session:
        plans = session.exec(select(MealPlan)).all()
        print(f"Total Meal Plans: {len(plans)}")
        
        items = session.exec(select(MealPlanItem)).all()
        print(f"Total Meal Plan Items: {len(items)}")
        
        if items:
            print("Sample Item:", items[0])

if __name__ == "__main__":
    verify_db()
