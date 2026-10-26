from pydantic import BaseModel
from typing import Optional, List, Literal

class Category(BaseModel):
    id: int
    name: str
class Tag(BaseModel):
    id: int
    name: str
class PetModel(BaseModel):
    id: int
    category: Optional[Category] = None
    name: str
    photoUrls: List[str]
    tags: Optional[List[Tag]] = None
    status: Literal["available", "pending", "sold"]
class ApiResponseModel(BaseModel):
    code: int
    type: str
    message: str