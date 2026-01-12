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
    weight: float  # in kg
    height: float  # in cm
    gender: Gender
    goal: Goal
    activity_level: float = Field(default=1.2)  # Multiplier


class MealPlan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    calories: int
    protein: int  # grams
    carbs: int  # grams
    fats: int  # grams
    name: str


class Food(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    calories: int
    protein: int  # grams
    carbs: int  # grams
    fats: int  # grams
    serving_size: str = Field(default="100g")


class MealType(str, Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"


class FoodSource(str, Enum):
    MANUAL = "manual"
    USDA = "usda"
    OFF = "off"


class FoodCategory(str, Enum):
    PROTEIN = "protein"
    CARB = "carb"
    FAT = "fat"
    VEGETABLE = "vegetable"
    FRUIT = "fruit"
    DAIRY = "dairy"
    MIXED = "mixed"


class FoodItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    calories: int
    protein: int  # grams
    carbs: int  # grams
    fats: int  # grams
    serving_size: str  # e.g. "100g" or "1 cup"

    # Classification
    category: FoodCategory = Field(default=FoodCategory.MIXED)

    # External Data
    # External Data
    source: FoodSource = Field(default=FoodSource.MANUAL)
    # USDA FDC ID or internal ref
    external_id: Optional[str] = Field(default=None)


class BrandedFood(SQLModel, table=True):
    """
    Separate table for Open Food Facts / Branded Products.
    Not directly used in MealPlan generation (for now).
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    brand: Optional[str] = Field(default=None)
    barcode: Optional[str] = Field(unique=True, index=True)

    # Macros per serving_size (usually normalized to 100g/ml from API)
    calories: int
    protein: int
    carbs: int
    fats: int
    serving_size: str = Field(default="100g")

    # Link back to OFF source just in case
    external_id: Optional[str] = Field(default=None)
    image_url: Optional[str] = Field(default=None)


class MealPlanItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    meal_plan_id: int = Field(foreign_key="mealplan.id")
    food_item_id: int = Field(foreign_key="fooditem.id")
    amount: float  # multiplier of serving size
    meal_type: MealType
