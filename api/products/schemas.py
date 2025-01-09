from typing import Any, Optional

from pydantic import BaseModel


class ProductCategoryCreate(BaseModel):
    name: str
    description: Optional[str]
    image: Optional[str] = None


class ProductCategoryResponse(ProductCategoryCreate):
    id: int


class ProductCreate(BaseModel):
    category_id: int
    name: str
    description: Optional[str] = ""
    price: float
    media: Optional[list[str]] = []


class ProductUpdate(ProductCreate):
    id: int
    name: Optional[str]
    category_id: Optional[int]
    price: Optional[float]


class ProductResponse(BaseModel):
    id: int
    category_id: int
    name: str
    description: Optional[str]
    price: float
    media: Optional[list[str]] = []
