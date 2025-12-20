from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum

class Goal(str, Enum):
    WEIGHT_LOSS = "weight_loss"
    MAINTENANCE = "maintenance"
    MUSCLE_GAIN = "muscle_gain"

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    age: int
    weight: float # in kg
    height: float # in cm
    gender: Gender
    goal: Goal
    activity_level: float = Field(default=1.2) # Multiplier

class MealPlan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    calories: int
    protein: int # grams
    carbs: int # grams
    fats: int # grams
    name: str
