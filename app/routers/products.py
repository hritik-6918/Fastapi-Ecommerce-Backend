from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.database.connection import get_database
from app.models.product import ProductCreate, ProductResponse

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", status_code=201, response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create a new product"""
    try:
        product_dict = product.dict()
        
        # Check if product with same name already exists
        existing_product = await db.products.find_one({"name": product.name})
        if existing_product:
            raise HTTPException(
                status_code=400, 
                detail="Product with this name already exists"
            )
        
        result = await db.products.insert_one(product_dict)
        created_product = await db.products.find_one({"_id": result.inserted_id})
        
        return ProductResponse(
            id=str(created_product["_id"]),
            name=created_product["name"],
            price=created_product["price"],
            quantity=created_product["quantity"]
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Failed to create product")

@router.get("/", response_model=List[ProductResponse])
async def list_products(
    name: Optional[str] = Query(None, description="Filter by product name (regex supported)"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    limit: Optional[int] = Query(10, ge=1, le=100, description="Number of products to return"),
    offset: Optional[int] = Query(0, ge=0, description="Number of products to skip"),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """List products with optional filtering and pagination"""
    try:
        # Build query
        query = {}
        
        if name:
            # Support regex/partial search (case insensitive)
            query["name"] = {"$regex": name, "$options": "i"}
        
        if min_price is not None or max_price is not None:
            price_query = {}
            if min_price is not None:
                price_query["$gte"] = min_price
            if max_price is not None:
                price_query["$lte"] = max_price
            query["price"] = price_query
        
        # Execute query with pagination
        cursor = db.products.find(query).skip(offset).limit(limit).sort("created_at", -1)
        products = await cursor.to_list(length=limit)
        
        # Transform to response format
        products_response = []
        for product in products:
            products_response.append(ProductResponse(
                id=str(product["_id"]),
                name=product["name"],
                price=product["price"],
                quantity=product["quantity"]
            ))
        
        return products_response
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch products")

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get a specific product by ID"""
    try:
        if not ObjectId.is_valid(product_id):
            raise HTTPException(status_code=400, detail="Invalid product ID")
        
        product = await db.products.find_one({"_id": ObjectId(product_id)})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return ProductResponse(
            id=str(product["_id"]),
            name=product["name"],
            price=product["price"],
            quantity=product["quantity"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch product")
