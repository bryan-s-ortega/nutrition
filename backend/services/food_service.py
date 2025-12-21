from typing import List
from sqlmodel import Session, select
from models import FoodItem, FoodSource
from integrations.usda import search_usda
from integrations.openfoodfacts import search_off
from database import engine

def search_food(query: str, usda_api_key: str = None) -> List[FoodItem]:
    """
    Search for food in local DB first, then external APIs.
    """
    results = []
    
    # 1. Search Local DB
    with Session(engine) as session:
        statement = select(FoodItem).where(FoodItem.name.contains(query)).limit(5)
        local_results = session.exec(statement).all()
        results.extend(local_results)

    # If we have enough local results, maybe return? 
    # For now, let's always fetch external to show "more" options.
    
    # 2. Search External APIs
    # Run sequentially for now
    usda_results = search_usda(query, usda_api_key)
    off_results = search_off(query)
    
    # 3. Combine
    results.extend(usda_results)
    results.extend(off_results)
    
    # Deduplication could go here (by name or external ID if we saved them previously)
    
    return results

def save_food_item(item: FoodItem, session: Session) -> FoodItem:
    """
    Save a selected external food item to the local database.
    """
    # Check if duplicate exists (by unique external_id if possible)
    if item.external_id:
        existing = session.exec(select(FoodItem).where(FoodItem.external_id == item.external_id)).first()
        if existing:
            return existing
            
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
