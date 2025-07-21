"""
Script to seed the database with sample data for testing
Run this after setting up your MongoDB connection
"""
import asyncio
import sys
import os

# Add the parent directory to the path so we can import our app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.connection import connect_to_mongo, close_mongo_connection, get_database

async def seed_products():
    """Seed the database with sample products"""
    await connect_to_mongo()
    db = await get_database()
    
    # Sample products
    sample_products = [
        {
            "name": "Laptop",
            "price": 999.99,
            "quantity": 10
        },
        {
            "name": "Smartphone",
            "price": 599.99,
            "quantity": 25
        },
        {
            "name": "Headphones",
            "price": 199.99,
            "quantity": 50
        },
        {
            "name": "Tablet",
            "price": 399.99,
            "quantity": 15
        },
        {
            "name": "Smart Watch",
            "price": 299.99,
            "quantity": 30
        }
    ]
    
    # Clear existing products (optional)
    await db.products.delete_many({})
    print("Cleared existing products")
    
    # Insert sample products
    result = await db.products.insert_many(sample_products)
    print(f"Inserted {len(result.inserted_ids)} products")
    
    # Print inserted products
    products = await db.products.find({}).to_list(length=None)
    for product in products:
        print(f"- {product['name']}: ${product['price']} (Qty: {product['quantity']}) [ID: {product['_id']}]")
    
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(seed_products())
