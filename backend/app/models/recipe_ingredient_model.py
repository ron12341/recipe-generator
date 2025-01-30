from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Float, nullable=False) # Amount of ingredient required (e.g. 1, 1.5, 2)
    unit = Column(String(100), nullable=False) # Unit of measurement (e.g. cups, tablespoons, grams)

    # Foreign keys
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)

    # Relationships
    recipe = relationship("Recipe", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="recipes")
