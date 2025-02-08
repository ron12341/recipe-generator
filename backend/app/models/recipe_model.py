from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)       # optional
    cuisine = Column(String, nullable=False)        # e.g. Italian, French, Japanese
    dietary = Column(JSON, nullable=False)  # e.g. [Vegetarian, Vegan]
    allergens = Column(JSON, nullable=False) # e.g. [Gluten, Dairy]
    recipe_type = Column(String, nullable=False)    # e.g. Lunch, Dinner
    difficulty = Column(String, nullable=False)     # e.g. easy, medium, hard
    cook_time = Column(JSON, nullable=False)        # {hours: int, minutes: int}
    instructions = Column(JSON, nullable=False)     # List of {step: int, title: string, description: string}
    servings = Column(JSON, nullable=False)         # {number: string, unit: string}  

    # Foreign key
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="recipes")
    ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")
