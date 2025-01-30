from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.recipe_schema import Recipe, RecipeCreate
from app.models.recipe_model import Recipe as RecipeModel
from app.models.user_model import User as UserModel
from app.core.auth import get_current_user

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
)

# Get all recipes
@router.get("/", response_model=List[Recipe])
async def get_recipes(db: Session = Depends(get_db)):
    recipes = db.query(RecipeModel).all()
    return recipes

# Get a Recipe by ID
@router.get("/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(RecipeModel).filter(RecipeModel.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

# Create a new recipe
@router.post("/", response_model=Recipe)
async def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
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

# fetch current user's recipes
@router.get("/user", response_model=List[Recipe])
async def get_my_recipes(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    recipes = db.query(RecipeModel).filter(RecipeModel.user_id == current_user.id).all()
    return recipes
