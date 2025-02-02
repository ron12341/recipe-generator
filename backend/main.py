from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db, drop_db
from app.routers import recipe_router, auth_router, user_router, profile_router
from app.core.database import Base, engine

# Initialize FastAPI app
app = FastAPI(
    title="Smart Recipe Generator",
    description="Generate recipes based on ingredients and preferences.",
    version="1.0.0",
)

# Allow CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown():
    drop_db()

@app.on_event("startup")
async def startup():
   init_db()

# Root Endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Smart Recipe Generator API!"}

# Include routers
app.include_router(recipe_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(profile_router)

