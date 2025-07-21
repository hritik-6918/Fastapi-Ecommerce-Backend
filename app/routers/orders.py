from fastapi import APIRouter, HTTPException, Depends, Query, Path
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.database.connection import get_database
from app.models.order import OrderCreate, OrderResponse, OrderItemResponse

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", status_code=201, response_model=OrderResponse)
async def create_order(
    order: OrderCreate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create a new order"""
    try:
        # Validate products exist and have enough quantity
        order_items = []
        total_calculated = 0
        
        for item in order.items:
            # Check if product exists
            if not ObjectId.is_valid(item.product_id):
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid product ID: {item.product_id}"
                )
            
            product = await db.products.find_one({"_id": ObjectId(item.product_id)})
            if not product:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Product not found: {item.product_id}"
                )
            
            # Check quantity availability
            if product["quantity"] < item.bought_quantity:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Insufficient quantity for product {product['name']}. Available: {product['quantity']}, Requested: {item.bought_quantity}"
                )
            
            # Calculate total
            item_total = product["price"] * item.bought_quantity
            total_calculated += item_total
            
            # Prepare order item
            order_items.append({
                "product_id": item.product_id,
                "bought_quantity": item.bought_quantity,
                "price": product["price"]
            })
        
        # Validate total amount (allow small floating point differences)
        if abs(total_calculated - order.total_amount) > 0.01:
            raise HTTPException(
                status_code=400, 
                detail=f"Total amount mismatch. Calculated: {total_calculated:.2f}, Provided: {order.total_amount:.2f}"
            )
        
        # Update product quantities (reduce inventory)
        for item in order.items:
            await db.products.update_one(
                {"_id": ObjectId(item.product_id)},
                {"$inc": {"quantity": -item.bought_quantity}}
            )
        
        # Create order document
        order_doc = {
            "user_id": "user123",  # In real app, get from authentication
            "items": order_items,
            "total_amount": order.total_amount,
            "user_address": order.user_address
        }
        
        result = await db.orders.insert_one(order_doc)
        created_order = await db.orders.find_one({"_id": result.inserted_id})
        
        # Transform response
        items_response = []
        for item in created_order["items"]:
            items_response.append(OrderItemResponse(
                product_id=item["product_id"],
                bought_quantity=item["bought_quantity"],
                price=item["price"]
            ))
        
        return OrderResponse(
            id=str(created_order["_id"]),
            items=items_response,
            total_amount=created_order["total_amount"],
            user_address=created_order["user_address"],
            created_at=created_order.get("created_at")
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create order")

@router.get("/{user_id}", response_model=List[OrderResponse])
async def get_user_orders(
    user_id: str = Path(..., description="User ID to get orders for"),
    limit: Optional[int] = Query(10, ge=1, le=100, description="Number of orders to return"),
    offset: Optional[int] = Query(0, ge=0, description="Number of orders to skip"),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get orders for a specific user with pagination"""
    try:
        query = {"user_id": user_id}
        
        # Get orders with pagination (newest first)
        cursor = db.orders.find(query).skip(offset).limit(limit).sort("created_at", -1)
        orders = await cursor.to_list(length=limit)
        
        # Transform to response format
        orders_response = []
        for order in orders:
            items_response = []
            for item in order["items"]:
                items_response.append(OrderItemResponse(
                    product_id=item["product_id"],
                    bought_quantity=item["bought_quantity"],
                    price=item["price"]
                ))
            
            orders_response.append(OrderResponse(
                id=str(order["_id"]),
                items=items_response,
                total_amount=order["total_amount"],
                user_address=order["user_address"],
                created_at=order.get("created_at")
            ))
        
        return orders_response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch user orders")

@router.get("/", response_model=List[OrderResponse])
async def get_all_orders(
    limit: Optional[int] = Query(10, ge=1, le=100, description="Number of orders to return"),
    offset: Optional[int] = Query(0, ge=0, description="Number of orders to skip"),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all orders with pagination (admin endpoint)"""
    try:
        # Get orders with pagination (newest first)
        cursor = db.orders.find({}).skip(offset).limit(limit).sort("created_at", -1)
        orders = await cursor.to_list(length=limit)
        
        # Transform to response format
        orders_response = []
        for order in orders:
            items_response = []
            for item in order["items"]:
                items_response.append(OrderItemResponse(
                    product_id=item["product_id"],
                    bought_quantity=item["bought_quantity"],
                    price=item["price"]
                ))
            
            orders_response.append(OrderResponse(
                id=str(order["_id"]),
                items=items_response,
                total_amount=order["total_amount"],
                user_address=order["user_address"],
                created_at=order.get("created_at")
            ))
        
        return orders_response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch orders")
