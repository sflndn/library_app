from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class Book(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "title": "Преступление и наказание",
                    "author": "Федор Достоевский",
                    "year": 1866,
                    "genre": "Роман",
                    "is_read": True,
                    "rating": 5,
                    "description": "Философский роман о моральных дилеммах"
                }
            ]
        }
    )

    id: int
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=1000, le=2025)
    genre: str = Field(..., min_length=1, max_length=50)
    is_read: bool = False
    rating: Optional[int] = Field(None, ge=1, le=5)
    description: Optional[str] = Field(None, max_length=500)


class BookCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "1984",
                    "author": "Джордж Оруэлл",
                    "year": 1949,
                    "genre": "Антиутопия",
                    "description": "Роман о тоталитарном обществе"
                }
            ]
        }
    )

    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=1000, le=2025)
    genre: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=500)


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1000, le=2025)
    genre: Optional[str] = Field(None, min_length=1, max_length=50)
    is_read: Optional[bool] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    description: Optional[str] = Field(None, max_length=500)