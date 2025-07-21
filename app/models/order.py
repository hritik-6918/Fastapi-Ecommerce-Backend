from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime
from bson import ObjectId
from app.models.product import PyObjectId

class OrderItem(BaseModel):
    product_id: str = Field(..., description="Product ID to order")
    bought_quantity: int = Field(..., gt=0, description="Quantity to purchase")

class OrderCreate(BaseModel):
    items: List[OrderItem] = Field(..., min_items=1, description="List of items to order")
    total_amount: float = Field(..., gt=0, description="Total order amount")
    user_address: Dict[str, Any] = Field(..., description="User delivery address")
    
    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "product_id": "507f1f77bcf86cd799439011",
                        "bought_quantity": 2
                    }
                ],
                "total_amount": 1999.98,
                "user_address": {
                    "street": "123 Main St",
                    "city": "New York",
                    "zip": "10001",
                    "country": "USA"
                }
            }
        }

class OrderItemResponse(BaseModel):
    product_id: str
    bought_quantity: int
    price: float

class OrderResponse(BaseModel):
    id: str
    items: List[OrderItemResponse]
    total_amount: float
    user_address: Dict[str, Any]
    created_at: datetime

class OrderInDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    items: List[Dict[str, Any]]
    total_amount: float
    user_address: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
