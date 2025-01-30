from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False) # e.g. "Vegetarian", "Vegan", etc 
    description = Column(Text, nullable=True)
    
    # Relationship
    users = relationship("User", secondary="user_preference_association", back_populates="preferences")