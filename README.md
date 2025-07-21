# FastAPI Ecommerce Backend

A comprehensive ecommerce backend API built with FastAPI and MongoDB for the HROne Backend Intern Hiring Task.

## 🚀 Features

- **Product Management**
  - Create new products
  - List products with filtering and pagination
  - Search products by name (regex support)
  - Filter by price range
  - Get individual product details

- **Order Management**
  - Create orders with inventory validation
  - Automatic inventory deduction
  - Get user orders with pagination
  - Get all orders (admin endpoint)
  - Order total validation

- **Technical Features**
  - Async/await support with Motor (MongoDB async driver)
  - Comprehensive input validation with Pydantic
  - Proper error handling and HTTP status codes
  - API documentation with Swagger/OpenAPI
  - CORS support for frontend integration
  - Database connection management

## 📋 Requirements

- Python 3.8+
- MongoDB Atlas account (free tier works)
- pip (Python package manager)

## 🛠️ Installation & Setup

### 1. Clone the Repository
\`\`\`bash
git clone <your-repo-url>
cd fastapi-ecommerce-backend
\`\`\`

### 2. Create Virtual Environment
\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

### 3. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Set Up MongoDB Atlas
1. Go to [MongoDB Atlas](https://cloud.mongodb.com)
2. Create a free M0 cluster
3. Create a database user with read/write permissions
4. Whitelist your IP address (or use 0.0.0.0/0 for development)
5. Get your connection string

### 5. Configure Environment Variables
Create a `.env` file in the root directory:
\`\`\`env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/ecommerce?retryWrites=true&w=majority
DATABASE_NAME=ecommerce
\`\`\`

### 6. Run the Application
\`\`\`bash
uvicorn app.main:app --reload
\`\`\`

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API Endpoints

### Products
- `POST /api/v1/products/` - Create a new product
- `GET /api/v1/products/` - List products with optional filtering
- `GET /api/v1/products/{product_id}` - Get a specific product

### Orders
- `POST /api/v1/orders/` - Create a new order
- `GET /api/v1/orders/{user_id}` - Get orders for a specific user
- `GET /api/v1/orders/` - Get all orders (admin)

### System
- `GET /` - API information
- `GET /health` - Health check

## 🧪 Testing

### Seed Sample Data
\`\`\`bash
python scripts/seed_data.py
\`\`\`

### Test API Endpoints
\`\`\`bash
python scripts/test_api.py
\`\`\`

### Manual Testing with curl

#### Create a Product:
\`\`\`bash
curl -X POST "http://localhost:8000/api/v1/products/" \
-H "Content-Type: application/json" \
-d '{
  "name": "Gaming Laptop",
  "price": 1299.99,
  "quantity": 5
}'
\`\`\`

#### List Products:
\`\`\`bash
curl "http://localhost:8000/api/v1/products/"
\`\`\`

#### Create an Order:
\`\`\`bash
curl -X POST "http://localhost:8000/api/v1/orders/" \
-H "Content-Type: application/json" \
-d '{
  "items": [
    {
      "product_id": "PRODUCT_ID_HERE",
      "bought_quantity": 1
    }
  ],
  "total_amount": 1299.99,
  "user_address": {
    "street": "123 Main St",
    "city": "New York",
    "zip": "10001",
    "country": "USA"
  }
}'
\`\`\`

## 🗄️ Database Schema

### Products Collection
\`\`\`json
{
  "_id": "ObjectId",
  "name": "string",
  "price": "number",
  "quantity": "number",
  "created_at": "datetime"
}
\`\`\`

### Orders Collection
\`\`\`json
{
  "_id": "ObjectId",
  "user_id": "string",
  "items": [
    {
      "product_id": "string",
      "bought_quantity": "number",
      "price": "number"
    }
  ],
  "total_amount": "number",
  "user_address": "object",
  "created_at": "datetime"
}
\`\`\`

## 🚀 Deployment

### Deploy to Render

1. **Prepare for Deployment**
   - Ensure your code is pushed to GitHub
   - Update `render.yaml` with your MongoDB connection string

2. **Deploy on Render**
   - Connect your GitHub repository to Render
   - Add environment variables in Render dashboard:
     - `MONGODB_URL`: Your MongoDB Atlas connection string
     - `DATABASE_NAME`: ecommerce
   - Deploy!

3. **Verify Deployment**
   - Check the health endpoint: `https://your-app.onrender.com/health`
   - Access API docs: `https://your-app.onrender.com/docs`

## 🏗️ Project Structure

\`\`\`
ecommerce-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── models/              # Pydantic models
│   │   ├── __init__.py
│   │   ├── product.py       # Product models
│   │   └── order.py         # Order models
│   ├── routers/             # API route handlers
│   │   ├── __init__.py
│   │   ├── products.py      # Product endpoints
│   │   └── orders.py        # Order endpoints
│   └── database/            # Database configuration
│       ├── __init__.py
│       └── connection.py    # MongoDB connection
├── scripts/                 # Utility scripts
│   ├── seed_data.py        # Database seeding
│   └── test_api.py         # API testing
├── requirements.txt         # Python dependencies
├── .env                    # Environment variables
├── render.yaml             # Render deployment config
└── README.md               # This file
\`\`\`

## 🔧 Development

### Code Quality
- Follow PEP 8 style guidelines
- Use type hints for better code documentation
- Implement proper error handling
- Write descriptive commit messages

### Adding New Features
1. Create new models in `app/models/`
2. Add route handlers in `app/routers/`
3. Update the main app in `app/main.py`
4. Add tests and documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is created for the HROne Backend Intern Hiring Task.

## 🆘 Support

If you encounter any issues:
1. Check the logs for error messages
2. Verify your MongoDB connection string
3. Ensure all environment variables are set correctly
4. Check the API documentation at `/docs`

---

**Built with ❤️ using FastAPI and MongoDB**
