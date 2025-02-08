from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth_service import get_current_user
from app.models.user_model import User as UserModel
from app.models.recipe_model import Recipe as RecipeModel
from app.models.recipe_ingredient_model import RecipeIngredient as RecipeIngredientModel
from app.schemas.recipe_schema import RecipeCreateRequest


def create_recipe(recipe: RecipeCreateRequest, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    new_recipe = RecipeModel(
        name=recipe.name,
        description=recipe.description or None,
        cuisine=recipe.cuisine,
        dietary=",".join(recipe.dietary),
        allergens=",".join(recipe.alergens),
        recipe_type=recipe.recipe_type,
        difficulty=recipe.difficulty,
        cook_time=recipe.cook_time,
        instructions=[instrcution for instrcution in recipe.instructions],
        servings=recipe.servings,
        user_id=current_user.id
    )

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    
    # Add Ingredients
    for ingredient in recipe.ingredients:
        new_ingredient = RecipeIngredientModel(
            recipe_id=new_recipe.id,
            name=ingredient.name,
            quantity=ingredient.quantity,
            unit=ingredient.unit
        )
        db.add(new_ingredient)
        db.commit()
        db.refresh(new_ingredient)

    return new_recipe