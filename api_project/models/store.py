from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class OrderModel(BaseModel):
    id: int
    petId: int
    quantity: int
    shipDate: Optional[datetime] = None
    status: Literal["placed", "approved", "delivered"]
    complete: bool