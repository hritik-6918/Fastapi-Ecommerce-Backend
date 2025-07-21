"""
Script to test the API endpoints
Make sure the server is running before executing this script
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_api():
    """Test all API endpoints"""
    
    print("=== Testing Product Endpoints ===")
    
    # Test creating a product
    print("\n1. Creating a new product...")
    product_data = {
        "name": "Test Product",
        "price": 99.99,
        "quantity": 5
    }
    
    try:
        response = requests.post(f"{BASE_URL}/products/", json=product_data)
        if response.status_code == 201:
            created_product = response.json()
            print(f"✅ Product created: {created_product}")
            product_id = created_product["id"]
        else:
            print(f"❌ Failed to create product: {response.status_code}")
            print(f"Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error creating product: {e}")
        return
    
    # Test listing products
    print("\n2. Listing all products...")
    try:
        response = requests.get(f"{BASE_URL}/products/")
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Found {len(products)} products")
            for product in products[:3]:  # Show first 3
                print(f"   - {product['name']}: ${product['price']}")
        else:
            print(f"❌ Failed to list products: {response.status_code}")
    except Exception as e:
        print(f"❌ Error listing products: {e}")
    
    # Test filtering products
    print("\n3. Filtering products by name...")
    try:
        response = requests.get(f"{BASE_URL}/products/?name=laptop")
        if response.status_code == 200:
            filtered_products = response.json()
            print(f"✅ Found {len(filtered_products)} products matching 'laptop'")
        else:
            print(f"❌ Failed to filter products: {response.status_code}")
    except Exception as e:
        print(f"❌ Error filtering products: {e}")
    
    print("\n=== Testing Order Endpoints ===")
    
    # Test creating an order
    print("\n4. Creating a new order...")
    order_data = {
        "items": [
            {
                "product_id": product_id,
                "bought_quantity": 2
            }
        ],
        "total_amount": 199.98,
        "user_address": {
            "street": "123 Test St",
            "city": "Test City",
            "zip": "12345",
            "country": "Test Country"
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/orders/", json=order_data)
        if response.status_code == 201:
            created_order = response.json()
            print(f"✅ Order created: {created_order['id']}")
            print(f"   Total: ${created_order['total_amount']}")
        else:
            print(f"❌ Failed to create order: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error creating order: {e}")
    
    # Test getting user orders
    print("\n5. Getting user orders...")
    try:
        response = requests.get(f"{BASE_URL}/orders/user123")
        if response.status_code == 200:
            user_orders = response.json()
            print(f"✅ Found {len(user_orders)} orders for user123")
        else:
            print(f"❌ Failed to get user orders: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting user orders: {e}")
    
    print("\n=== API Testing Complete ===")

if __name__ == "__main__":
    test_api()

