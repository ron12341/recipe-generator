from pydantic import BaseModel
from typing import Optional, List
from .recipe_components_schema import Instruction, Serving, CookTime
from .ingredient_schema import IngredientResponse


class RecipeCreateRequest(BaseModel):
    name: str
    description: Optional[str]
    cuisine: str
    dietary: List[str]
    allergens: List[str]
    recipe_type: str
    difficulty: str
    cook_time: CookTime
    instructions: List[Instruction]
    servings: Serving
    user_id: str
    
class RecipeGenerateRequest(BaseModel):
    cuisine: str
    dietary: List[str]
    recipe_type: str
    allergens: List[str]
    ingredients: List[str]  # List of ingredient names

class RecipeUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    instructions: Optional[str]
    cooking_time: Optional[int]
    difficulty: Optional[str]
    servings: Optional[int]

class RecipeResponse(BaseModel):
    name: str
    description: str
    cuisine: str
    dietary: List[str]
    allergens: List[str]
    recipe_type: str
    difficulty: str
    cook_time: CookTime
    instructions: List[Instruction]
    servings: Serving

    class Config:
        orm_mode = True

    @classmethod
    def from_json(cls, json_data: dict):

        try:
            cook_time_data = json_data["cook_time"]
            cook_time = CookTime(hours=cook_time_data["hours"], minutes=cook_time_data["minutes"])

            servings_data = json_data["servings"]
            servings = Serving(number=servings_data["number"], unit=servings_data["unit"])

            # ingredients = [IngredientResponse(ingredient["name"], ingredient["quantity"]. ingredient["unit"]) for ingredient in json_data["ingredients"]]

            instructions = [Instruction(step=instruction["step"], title=instruction["title"], description=instruction["description"]) for instruction in json_data["instructions"]]

            return cls(
                name=json_data["name"],
                description=json_data["description"],
                cuisine=json_data["cuisine"],
                dietary=json_data["dietary"],
                allergens=json_data["allergens"],
                recipe_type=json_data["recipe_type"],
                difficulty=json_data["difficulty"],
                cook_time=cook_time,
                instructions=instructions,
                servings=servings
            )

        except Exception as e:
            print(f"Error converting JSON to Recipe: {e}")
            return None
