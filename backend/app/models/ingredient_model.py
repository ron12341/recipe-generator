from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False) # Name of the ingredient (e.g., "Tomato")
    description = Column(Text, nullable=True)   # Description of the ingredient (optional)
    
    # Relationships
    recipes = relationship("RecipeIngredient", back_populates="ingredient")