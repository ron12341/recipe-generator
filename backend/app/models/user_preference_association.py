from sqlalchemy import Column, ForeignKey, Integer, Table
from unittest.mock import Base

"""
Define a many-to-many association table linking users and preferences
"""
user_preference_association = Table(
    "user_preference_association",

    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("preference_id", Integer, ForeignKey("preferences.id"), primary_key=True),
)