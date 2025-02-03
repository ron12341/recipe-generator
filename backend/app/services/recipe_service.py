from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from app.models.recipe_model import Recipe as RecipeModel
from app.schemas.recipe_schema import RecipeCreate, RecipeUpdate
from app.core.database import get_db
from app.models.user_model import User as UserModel
from app.services.auth_service import get_current_user


def get_all_recipes(db: Session = Depends(get_db)) -> List[RecipeModel]:
    recipes = db.query(RecipeModel).all()
    return recipes

def get_recipes_by_user(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)) -> List[RecipeModel]:
    recipes = db.query(RecipeModel).filter(RecipeModel.user_id == current_user.id).all()
    return recipes

def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    new_recipe = RecipeModel(
        name=recipe.name,
        description=recipe.description,
        instructions=recipe.instructions,
        cooking_time=recipe.cooking_time,
        difficulty=recipe.difficulty,
        rating=recipe.rating,
        servings=recipe.servings,
        user_id=current_user.id
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe

