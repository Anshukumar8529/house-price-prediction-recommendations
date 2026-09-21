import os
import pickle
import pandas as pd
from typing import Dict, Any, List
from fastapi import HTTPException
from backend.schemas import AnalyticsSummaryResponse


class AnalyticsService:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.viz_df: pd.DataFrame = None
        self.sector_features: Dict[str, str] = {}
        self.is_loaded: bool = False

    def load_analytics_data(self):
        """Loads visualization CSV and sector wordcloud dictionary into memory."""
        csv_path = os.path.join(self.data_dir, "data_viz1.csv")
        wc_path = os.path.join(self.data_dir, "sector_wordcloud.pkl")

        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Visualization dataset not found at {csv_path}")
        if not os.path.exists(wc_path):
            raise FileNotFoundError(f"Wordcloud artifact not found at {wc_path}")

        try:
            self.viz_df = pd.read_csv(csv_path)

            with open(wc_path, "rb") as f:
                self.sector_features = pickle.load(f)

            self.is_loaded = True
            print("Successfully loaded analytics dataset (data_viz1.csv) and wordcloud pickle.")
        except Exception as e:
            raise RuntimeError(f"Error loading analytics data: {str(e)}")

    def get_summary(self) -> AnalyticsSummaryResponse:
        """Computes key property market analytics metrics."""
        if not self.is_loaded or self.viz_df is None:
            raise HTTPException(status_code=500, detail="Analytics service is not initialized.")

        total_props = int(len(self.viz_df))
        avg_p = float(self.viz_df["price"].mean()) if "price" in self.viz_df.columns else 0.0
        min_p = float(self.viz_df["price"].min()) if "price" in self.viz_df.columns else 0.0
        max_p = float(self.viz_df["price"].max()) if "price" in self.viz_df.columns else 0.0

        avg_pps = float(self.viz_df["price_per_sqft"].mean()) if "price_per_sqft" in self.viz_df.columns else 0.0
        avg_bua = float(self.viz_df["built_up_area"].mean()) if "built_up_area" in self.viz_df.columns else 0.0

        type_counts = self.viz_df["property_type"].value_counts().to_dict() if "property_type" in self.viz_df.columns else {}

        return AnalyticsSummaryResponse(
            total_properties=total_props,
            avg_price=round(avg_p, 2),
            min_price=round(min_p, 2),
            max_price=round(max_p, 2),
            avg_price_per_sqft=round(avg_pps, 2),
            avg_built_up_area=round(avg_bua, 2),
            property_type_counts={str(k): int(v) for k, v in type_counts.items()}
        )

    def get_wordcloud_sectors(self) -> List[str]:
        if not self.is_loaded:
            return []
        return sorted(list(self.sector_features.keys()))

    def get_wordcloud_text(self, sector: str) -> str:
        if not self.is_loaded:
            raise HTTPException(status_code=500, detail="Analytics service not loaded.")
        if sector not in self.sector_features:
            raise HTTPException(status_code=404, detail=f"Sector '{sector}' not found in wordcloud dataset.")
        return self.sector_features[sector]

    def get_raw_viz_data(self) -> List[Dict[str, Any]]:
        if not self.is_loaded or self.viz_df is None:
            return []
        return self.viz_df.to_dict(orient="records")

    def get_geomap_data(self) -> List[Dict[str, Any]]:
        if not self.is_loaded or self.viz_df is None:
            return []
        group_df = self.viz_df.groupby("sector")[
            ["price", "price_per_sqft", "built_up_area", "latitude", "longitude"]
        ].mean().reset_index()
        return group_df.to_dict(orient="records")
