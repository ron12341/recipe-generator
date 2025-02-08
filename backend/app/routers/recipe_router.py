from openai import OpenAI
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.recipe_schema import RecipeResponse, RecipeGenerateRequest
from app.models.recipe_model import Recipe as RecipeModel
from app.models.user_model import User as UserModel
from app.services.auth_service import get_current_user
from app.core.config import settings
import json

OPENAI_API_KEY = settings.OPENAI_API_KEY

RECIPE = '''
{
    "name": "Tomato Ketchup Pasta",
    "description": "A quick and unique Italian-inspired breakfast pasta made with fresh tomatoes and a tangy ketchup sauce, perfect for a hearty start to your day.",        
    "difficulty": "easy",
    "cuisine": "Italian",
    "dietary": [
        "Vegetarian",
        "Vegan"
    ],
    "allergens": [
        "Gluten"
    ],
    "recipe_type": "breakfast",
    "servings": {
        "number": "4",
        "unit": "servings"
    },
    "cook_time": {
        "hours": "0",
        "minutes": "30"
    },
    "ingredients": [
        {
            "name": "Pasta",
            "quantity": "300",
            "unit": "grams"
        },
        {
            "name": "Fresh tomatoes",
            "quantity": "4",
            "unit": "medium"
        },
        {
            "name": "Ketchup",
            "quantity": "1/2",
            "unit": "cup"
        },
        {
            "name": "Olive oil",
            "quantity": "2",
            "unit": "tablespoons"
        },
        {
            "name": "Garlic",
            "quantity": "2",
            "unit": "cloves"
        },
        {
            "name": "Basil leaves",
            "quantity": "1/4",
            "unit": "cup"
        },
        {
            "name": "Salt",
            "quantity": "to taste",
            "unit": ""
        },
        {
            "name": "Black pepper",
            "quantity": "to taste",
            "unit": ""
        }
    ],
    "instructions": [
        {
            "step": "1",
            "title": "Cook the Pasta",
            "description": "Bring a large pot of salted water to a boil. Add the pasta and cook according to package instructions until al dente. Drain and set aside."      
        },
        {
            "step": "2",
            "title": "Prepare the Tomato Sauce",
            "description": "In a large skillet, heat the olive oil over medium heat. Add minced garlic and sauté for about 1-2 minutes until fragrant."
        },
        {
            "step": "3",
            "title": "Add Fresh Tomatoes",
            "description": "Chop the fresh tomatoes and add them to the skillet. Cook for about 5-7 minutes until they soften and release their juices."
        },
        {
            "step": "4",
            "title": "Mix in Ketchup",
            "description": "Stir in the ketchup and mix well. Let it simmer for another 2-3 minutes. Season with salt and black pepper to taste."
        },
        {
            "step": "5",
            "title": "Combine Pasta and Sauce",
            "description": "Add the cooked pasta to the skillet and toss until the pasta is well coated with the sauce. Remove from heat."
        },
        {
            "step": "6",
            "title": "Garnish and Serve",
            "description": "Chop fresh basil leaves and sprinkle them over the pasta. Serve hot and enjoy your unique breakfast dish!"
        }
    ]
}
'''

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
)

# Get all recipes
@router.get("/", response_model=List[RecipeResponse])
async def get_recipes(db: Session = Depends(get_db)):
    recipes = db.query(RecipeModel).all()
    return recipes

# Get a Recipe by ID
@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(RecipeModel).filter(RecipeModel.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

# Create a new recipe

@router.post("/generate-recipe", response_model=RecipeResponse)
async def generate_recipe(request: RecipeGenerateRequest, db: Session = Depends(get_db)):
    try:

        prompt = f"""
        Generate a detailed {request.cuisine} recipe using the following ingredients: {', '.join(request.ingredients)}.
        The recipe should be {request.recipe_type} and should have the following dietary restrictions: {', '.join(request.dietary)}.
        The recipe should have the following allergens: {', '.join(request.allergens)}.
        
        Return the response in the following JSON Format:
        {{
            "name": "Recipe Name",
            "description": "Recipe Description",
            "difficulty": "easy | medium | hard",
            "cuisine": "Italian",
            "dietary": [
                "Vegetarian",
                "Vegan"
            ],
            "allergens": [
                "Gluten"
            ],
            "recipe_type": "breakfast | lunch | dinner | snack | dessert",
            "servings": {{
                "number": "4",
                "unit": "servings"
            }}
            "cook_time": {{
                "hours": "2",
                "minutes": "30"
            }},
            "ingredients": [
                {{
                    "name": "Ingredient Name",
                    "quantity": "1 cup",
                    "unit": "grams"
                }}
            ],
            "instructions": [
            {{
                "step": "1",
                "title": "Step Title",
                "description": "Step Description"
            }}
            ]
        }}

        Remove the JSON wrapper from the response
        """

        # client = OpenAI()
        # response = client.chat.completions.create(
        #     model="gpt-4o-mini",
        #     messages=[
        #         {"role": "system", "content": "You are a professional chef"},
        #         {"role": "user", "content": prompt}
        #     ],
        #     temperature=0.7,
        #     max_tokens=1000,
        #     top_p=1,
        #     frequency_penalty=0,
        #     presence_penalty=0,
        # )
        
        # recipe_text = response.choices[0].message.content   # String JSON
        # print(recipe_text)

        # recipe_data = json.loads(recipe_text)
        # recipe_response = RecipeResponse.from_json(recipe_data)
        # return recipe_response

        recipe_response = RecipeResponse.from_json(json.loads(RECIPE))
        return recipe_response

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")


# fetch current user's recipes
@router.get("/user", response_model=List[RecipeResponse])
async def get_my_recipes(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    recipes = db.query(RecipeModel).filter(RecipeModel.user_id == current_user.id).all()
    return recipes

