from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database.connection import connect_to_mongo, close_mongo_connection
from app.routers import products, orders

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title="Ecommerce Backend API",
    description="A comprehensive ecommerce backend built with FastAPI and MongoDB for HROne Backend Intern Hiring Task",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Ecommerce Backend API is running!",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "ecommerce-backend",
        "version": "1.0.0"
    }
