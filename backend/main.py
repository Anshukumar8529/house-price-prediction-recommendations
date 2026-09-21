import os
from contextlib import asynccontextmanager
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.schemas import (
    HealthResponse,
    PredictionRequest,
    PredictionResponse,
    RecommendationRequest,
    RecommendationResponse,
    RadiusSearchRequest,
    RadiusSearchResponse,
    AnalyticsSummaryResponse,
    OptionsResponse
)
from backend.model_service import ModelService
from backend.recommendation_service import RecommendationService
from backend.analytics_service import AnalyticsService

# Instantiating domain services
model_service = ModelService(data_dir="data")
recommendation_service = RecommendationService(data_dir="data")
analytics_service = AnalyticsService(data_dir="data")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager to load ML models, recommendation matrices,
    and dataset files into memory EXACTLY ONCE when FastAPI application starts up.
    """
    print("Initializing Real Estate Price Prediction & Recommendation Backend Services...")
    try:
        model_service.load_model_and_data()
        recommendation_service.load_recommendation_data()
        analytics_service.load_analytics_data()
        print("All ML models, dataset pickles, and recommendation matrices loaded into memory.")
    except Exception as e:
        print(f"CRITICAL: Service initialization failed during startup: {str(e)}")
        raise e

    yield  # Application serves requests here

    print("Shutting down FastAPI backend application and releasing resources.")


# Initialize FastAPI application
app = FastAPI(
    title="Real Estate House Price Prediction & Recommendation System API",
    description="Production-style REST API providing machine learning price predictions, content-based property recommendations, radius location searching, and real estate market analytics.",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from Streamlit, Web clients, Mobile, etc.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom Global Exception Handler for friendly JSON errors
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail
        }
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": f"An unexpected internal error occurred: {str(exc)}"
        }
    )


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    1. Health Check Endpoint
    Returns system status and operational message.
    """
    return HealthResponse(
        status="success",
        message="House Price Prediction API is running"
    )


@app.get("/options", response_model=OptionsResponse, tags=["Metadata"])
async def get_options():
    """
    Returns dropdown selection options for forms (sectors, property types, apartment names, etc.)
    """
    opts = model_service.get_dropdown_options()
    opts.apartment_names = recommendation_service.get_apartment_names()
    opts.locations = recommendation_service.get_locations()
    return opts


@app.post("/predict", response_model=PredictionResponse, tags=["Machine Learning"])
async def predict_price(request: PredictionRequest):
    """
    2. House Price Prediction Endpoint
    Accepts property input features, validates them using Pydantic,
    and runs the scikit-learn ML pipeline to estimate property value in Crores.
    """
    return model_service.predict(request)


@app.post("/recommend", response_model=RecommendationResponse, tags=["Recommendations"])
async def get_recommendations(request: RecommendationRequest):
    """
    3. Property Recommendations Endpoint (By Apartment Name)
    Accepts a property name and returns top N recommended properties based on cosine similarity matrices.
    """
    return recommendation_service.get_recommendations(request)


@app.post("/recommend/radius", response_model=RadiusSearchResponse, tags=["Recommendations"])
async def search_by_radius(request: RadiusSearchRequest):
    """
    Radius Location Search Endpoint
    Accepts a target location/sector and radius in km, returning nearby locations within distance.
    """
    return recommendation_service.search_by_radius(request)


@app.get("/analytics", response_model=AnalyticsSummaryResponse, tags=["Analytics"])
async def get_analytics_summary():
    """
    4. Property Analytics Summary Endpoint
    Returns total properties count, average/min/max prices, average price per sqft, and property type breakdown.
    """
    return analytics_service.get_summary()


@app.get("/analytics/geomap", tags=["Analytics"])
async def get_geomap_data():
    """Returns sector-wise aggregated price and location coordinates for mapping."""
    return analytics_service.get_geomap_data()


@app.get("/analytics/wordcloud/{sector}", tags=["Analytics"])
async def get_sector_wordcloud(sector: str):
    """Returns feature wordcloud text string for a given sector."""
    text = analytics_service.get_wordcloud_text(sector)
    return {"status": "success", "sector": sector, "text": text}


@app.get("/analytics/wordcloud-sectors", tags=["Analytics"])
async def get_wordcloud_sectors():
    """Returns list of available sectors for wordcloud generation."""
    sectors = analytics_service.get_wordcloud_sectors()
    return {"status": "success", "sectors": sectors}


@app.get("/analytics/raw", tags=["Analytics"])
async def get_raw_viz_data():
    """Returns raw visualization dataset rows."""
    return analytics_service.get_raw_viz_data()
