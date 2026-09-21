import os
import pickle
import pandas as pd
import numpy as np
from typing import List, Tuple
from fastapi import HTTPException
from backend.schemas import (
    RecommendationRequest,
    RecommendationResponse,
    RecommendationItem,
    RadiusSearchRequest,
    RadiusSearchResponse,
    RadiusSearchResultItem
)


class RecommendationService:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.location_df: pd.DataFrame = None
        self.cosine_sim1: np.ndarray = None
        self.cosine_sim2: np.ndarray = None
        self.cosine_sim3: np.ndarray = None
        self.cosine_sim_matrix: np.ndarray = None
        self.is_loaded: bool = False

    def load_recommendation_data(self):
        """Loads recommendation datasets and cosine similarity matrices into memory once."""
        loc_path = os.path.join(self.data_dir, "location_distance.pkl")
        sim1_path = os.path.join(self.data_dir, "cosine_sim1.pkl")
        sim2_path = os.path.join(self.data_dir, "cosine_sim2.pkl")
        sim3_path = os.path.join(self.data_dir, "cosine_sim3.pkl")

        for path in [loc_path, sim1_path, sim2_path, sim3_path]:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Recommendation artifact missing at {path}")

        try:
            with open(loc_path, "rb") as f:
                self.location_df = pickle.load(f)

            with open(sim1_path, "rb") as f:
                self.cosine_sim1 = pickle.load(f)

            with open(sim2_path, "rb") as f:
                self.cosine_sim2 = pickle.load(f)

            with open(sim3_path, "rb") as f:
                self.cosine_sim3 = pickle.load(f)

            # Pre-compute weighted composite cosine similarity matrix once
            self.cosine_sim_matrix = (
                30 * self.cosine_sim1
                + 20 * self.cosine_sim2
                + 8 * self.cosine_sim3
            )
            self.is_loaded = True
            print("Successfully loaded recommendation data and calculated cosine similarity matrix.")
        except Exception as e:
            raise RuntimeError(f"Failed to load recommendation data: {str(e)}")

    def get_apartment_names(self) -> List[str]:
        if not self.is_loaded or self.location_df is None:
            return []
        return sorted(self.location_df.index.tolist())

    def get_locations(self) -> List[str]:
        if not self.is_loaded or self.location_df is None:
            return []
        return sorted(self.location_df.columns.tolist())

    def get_recommendations(self, req: RecommendationRequest) -> RecommendationResponse:
        """Finds top N similar properties for a given property name."""
        if not self.is_loaded:
            raise HTTPException(status_code=500, detail="Recommendation engine is not initialized.")

        property_name = req.property_name
        if property_name not in self.location_df.index:
            raise HTTPException(
                status_code=404,
                detail=f"Property '{property_name}' not found in recommendation dataset."
            )

        try:
            idx = self.location_df.index.get_loc(property_name)
            sim_scores = list(enumerate(self.cosine_sim_matrix[idx]))
            sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            top_n = req.top_n
            top_indices = [i[0] for i in sorted_scores[1: top_n + 1]]
            top_scores = [float(i[1]) for i in sorted_scores[1: top_n + 1]]
            top_properties = self.location_df.index[top_indices].tolist()

            items = [
                RecommendationItem(
                    property_name=p,
                    similarity_score=round(s, 4)
                )
                for p, s in zip(top_properties, top_scores)
            ]

            return RecommendationResponse(
                status="success",
                target_property=property_name,
                recommendations=items
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Recommendation computation failed: {str(e)}")

    def search_by_radius(self, req: RadiusSearchRequest) -> RadiusSearchResponse:
        """Searches locations within a given radius in kilometers."""
        if not self.is_loaded:
            raise HTTPException(status_code=500, detail="Recommendation service not loaded.")

        location = req.location
        if location not in self.location_df.columns:
            raise HTTPException(
                status_code=404,
                detail=f"Location '{location}' not found in location matrix."
            )

        try:
            radius_meters = req.radius_km * 1000.0
            filtered = self.location_df[self.location_df[location] < radius_meters][location].sort_values()

            items = [
                RadiusSearchResultItem(
                    location_name=str(loc_name),
                    distance_km=round(float(dist_m) / 1000.0, 2)
                )
                for loc_name, dist_m in filtered.items()
            ]

            return RadiusSearchResponse(
                status="success",
                selected_location=location,
                radius_km=req.radius_km,
                results=items
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Radius search failed: {str(e)}")
