from fastapi import APIRouter, Depends, Query
from typing import List, Optional
import os
from sqlmodel import Session
from database import get_session
from models import FoodItem
from services.food_service import search_food, save_food_item

router = APIRouter()

@router.get("/food/search", response_model=List[FoodItem])
def search_food_endpoint(q: str):
    api_key = os.getenv("USDA_API_KEY")
    results = search_food(q, api_key)
    return results

@router.post("/food/save", response_model=FoodItem)
def save_food_endpoint(item: FoodItem, session: Session = Depends(get_session)):
    saved_item = save_food_item(item, session)
    return saved_item
