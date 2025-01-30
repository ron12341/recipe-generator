from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models import User


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=False)
    cooking_time = Column(Integer, nullable=False) # in minutes
    difficulty = Column(String, nullable=False) # e.g. easy, medium, hard
    rating = Column(Float, default=0.0)
    servings = Column(Integer, nullable=False)

    # Foreign key
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="recipes")
    ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")
