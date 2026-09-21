import os
import pickle
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from fastapi import HTTPException
from backend.schemas import PredictionRequest, PredictionResponse, OptionsResponse


class ModelService:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.df: pd.DataFrame = None
        self.pipeline: Any = None
        self.is_loaded: bool = False

    def load_model_and_data(self):
        """Loads dataset and pre-trained prediction pipeline into memory once."""
        df_path = os.path.join(self.data_dir, "df.pkl")
        pipeline_path = os.path.join(self.data_dir, "pipeline.pkl")

        if not os.path.exists(df_path):
            raise FileNotFoundError(f"Dataset file not found at {df_path}")
        if not os.path.exists(pipeline_path):
            raise FileNotFoundError(f"Model pipeline file not found at {pipeline_path}")

        try:
            with open(df_path, "rb") as f:
                self.df = pickle.load(f)

            with open(pipeline_path, "rb") as f:
                self.pipeline = pickle.load(f)

            self.is_loaded = True
            print("Successfully loaded dataset (df.pkl) and ML pipeline (pipeline.pkl)")
        except Exception as e:
            raise RuntimeError(f"Error loading model files: {str(e)}")

    def get_dropdown_options(self) -> OptionsResponse:
        """Extracts unique value dropdown options from df.pkl for frontend forms."""
        if not self.is_loaded or self.df is None:
            raise HTTPException(status_code=500, detail="Model service not initialized.")

        return OptionsResponse(
            property_types=["flat", "house"],
            sectors=sorted(self.df["sector"].astype(str).unique().tolist()),
            bedrooms=[float(x) for x in sorted(self.df["bedRoom"].dropna().unique().tolist())],
            bathrooms=[float(x) for x in sorted(self.df["bathroom"].dropna().unique().tolist())],
            balconies=[str(x) for x in sorted(self.df["balcony"].dropna().unique().tolist())],
            age_possessions=[str(x) for x in sorted(self.df["agePossession"].dropna().unique().tolist())],
            furnishing_types=[str(x) for x in sorted(self.df["furnishing_type"].dropna().unique().tolist())],
            luxury_categories=[str(x) for x in sorted(self.df["luxury_category"].dropna().unique().tolist())],
            floor_categories=[str(x) for x in sorted(self.df["floor_category"].dropna().unique().tolist())],
            apartment_names=[],
            locations=[]
        )

    def predict(self, req: PredictionRequest) -> PredictionResponse:
        """Executes price prediction pipeline given structured input."""
        if not self.is_loaded or self.pipeline is None:
            raise HTTPException(
                status_code=500,
                detail="ML model pipeline is not loaded in memory."
            )

        # Validate categorical values against dataset domains if appropriate
        if req.property_type not in ["flat", "house"]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid property_type '{req.property_type}'. Must be 'flat' or 'house'."
            )

        data = [[
            req.property_type,
            req.sector,
            req.bedRoom,
            req.bathroom,
            req.balcony,
            req.agePossession,
            req.built_up_area,
            req.servant_room,
            req.store_room,
            req.furnishing_type,
            req.luxury_category,
            req.floor_category
        ]]

        columns = [
            "property_type",
            "sector",
            "bedRoom",
            "bathroom",
            "balcony",
            "agePossession",
            "built_up_area",
            "servant room",
            "store room",
            "furnishing_type",
            "luxury_category",
            "floor_category"
        ]

        try:
            one_df = pd.DataFrame(data, columns=columns)
            predicted_log_price = self.pipeline.predict(one_df)[0]
            base_price = float(np.expm1(predicted_log_price))

            low = round(base_price - 0.22, 2)
            high = round(base_price + 0.22, 2)
            base_price_rounded = round(base_price, 2)

            return PredictionResponse(
                status="success",
                predicted_price_cr=base_price_rounded,
                price_range_low_cr=max(0.0, low),
                price_range_high_cr=high,
                formatted_range=f"The estimated price is between {max(0.0, low):.2f} Cr and {high:.2f} Cr (Base: {base_price_rounded:.2f} Cr)"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Prediction pipeline execution failed: {str(e)}"
            )
