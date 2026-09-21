from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class HealthResponse(BaseModel):
    status: str = "success"
    message: str = "House Price Prediction & Recommendation API is running"


class PredictionRequest(BaseModel):
    property_type: str = Field(..., example="flat", description="Type of property: 'flat' or 'house'")
    sector: str = Field(..., example="sector 102", description="Sector name matching dataset sectors")
    bedRoom: float = Field(..., gt=0, example=3.0, description="Number of bedrooms (> 0)")
    bathroom: float = Field(..., gt=0, example=2.0, description="Number of bathrooms (> 0)")
    balcony: str = Field(..., example="2", description="Balcony count/category ('0', '1', '2', '3', '3+')")
    agePossession: str = Field(..., example="Relatively New", description="Age or possession status")
    built_up_area: float = Field(..., gt=0, example=1500.0, description="Built-up area in square feet (> 0)")
    servant_room: float = Field(default=0.0, ge=0.0, le=1.0, example=0.0, description="Servant room flag: 0.0 or 1.0")
    store_room: float = Field(default=0.0, ge=0.0, le=1.0, example=0.0, description="Store room flag: 0.0 or 1.0")
    furnishing_type: str = Field(..., example="semi-furnished", description="Furnishing type")
    luxury_category: str = Field(..., example="Medium", description="Luxury level category")
    floor_category: str = Field(..., example="Mid Floor", description="Floor level category")


class PredictionResponse(BaseModel):
    status: str = "success"
    predicted_price_cr: float = Field(..., description="Base predicted price in Crores (Cr)")
    price_range_low_cr: float = Field(..., description="Estimated lower bound price in Cr")
    price_range_high_cr: float = Field(..., description="Estimated upper bound price in Cr")
    formatted_range: str = Field(..., description="Human-readable price range string")


class RecommendationRequest(BaseModel):
    property_name: str = Field(..., example="Emaar MGF Emerald Floors Premier", description="Selected apartment/property name")
    top_n: int = Field(default=5, gt=0, le=20, description="Number of recommended properties to return")


class RecommendationItem(BaseModel):
    property_name: str
    similarity_score: float


class RecommendationResponse(BaseModel):
    status: str = "success"
    target_property: str
    recommendations: List[RecommendationItem]


class RadiusSearchRequest(BaseModel):
    location: str = Field(..., example="sector 102", description="Location/sector column name in location matrix")
    radius_km: float = Field(..., ge=0.0, description="Search radius in kilometers")


class RadiusSearchResultItem(BaseModel):
    location_name: str
    distance_km: float


class RadiusSearchResponse(BaseModel):
    status: str = "success"
    selected_location: str
    radius_km: float
    results: List[RadiusSearchResultItem]


class AnalyticsSummaryResponse(BaseModel):
    total_properties: int
    avg_price: float
    min_price: float
    max_price: float
    avg_price_per_sqft: float
    avg_built_up_area: float
    property_type_counts: Dict[str, int]


class OptionsResponse(BaseModel):
    property_types: List[str]
    sectors: List[str]
    bedrooms: List[float]
    bathrooms: List[float]
    balconies: List[str]
    age_possessions: List[str]
    furnishing_types: List[str]
    luxury_categories: List[str]
    floor_categories: List[str]
    apartment_names: List[str]
    locations: List[str]
