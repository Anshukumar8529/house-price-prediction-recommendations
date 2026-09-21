import os
import streamlit as st
import requests
import pandas as pd

API_URL = os.getenv("API_URL", os.getenv("BACKEND_URL", "http://127.0.0.1:8000")).rstrip("/")

st.set_page_config(page_title="Price Prediction", page_icon="📈", layout="wide")

st.title("🏠 Real Estate Price Predictor")
st.markdown("*(Powered by FastAPI Backend & Scikit-Learn ML Pipeline)*")


# Fetch dropdown options from FastAPI backend
@st.cache_data(ttl=600)
def get_options():
    try:
        response = requests.get(f"{API_URL}/options", timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception:
        st.error(f"⚠️ Could not connect to FastAPI server at `{API_URL}`. Please start uvicorn backend.")
        st.info("Run: `uvicorn backend.main:app --reload`")
        return None
    return None

options = get_options()

if options is None:
    st.stop()

st.header("Enter Property Inputs")

col1, col2 = st.columns(2)

with col1:
    property_type = st.selectbox(
        "Property Type",
        options.get("property_types", ["flat", "house"])
    )

    sector = st.selectbox(
        "Sector",
        options.get("sectors", [])
    )

    bedrooms = float(
        st.selectbox(
            "Number of Bedrooms",
            options.get("bedrooms", [1.0, 2.0, 3.0, 4.0, 5.0])
        )
    )

    bathrooms = float(
        st.selectbox(
            "Number of Bathrooms",
            options.get("bathrooms", [1.0, 2.0, 3.0, 4.0])
        )
    )

    balcony = st.selectbox(
        "Number of Balconies",
        options.get("balconies", ["0", "1", "2", "3", "3+"])
    )

    property_age = st.selectbox(
        "Property Age",
        options.get("age_possessions", [])
    )

with col2:
    built_up_area = float(
        st.number_input("Built-up Area in sqft", min_value=10.0, value=1500.0, step=50.0)
    )

    servant_room = float(
        st.selectbox(
            "Servant Room",
            [0.0, 1.0],
            format_func=lambda x: "Yes" if x == 1.0 else "No"
        )
    )

    store_room = float(
        st.selectbox(
            "Store Room",
            [0.0, 1.0],
            format_func=lambda x: "Yes" if x == 1.0 else "No"
        )
    )

    furnishing_type = st.selectbox(
        "Furnishing Type",
        options.get("furnishing_types", [])
    )

    luxury_category = st.selectbox(
        "Luxury Category",
        options.get("luxury_categories", [])
    )

    floor_category = st.selectbox(
        "Floor Category",
        options.get("floor_categories", [])
    )


def format_property_details(payload: dict) -> pd.DataFrame:
    """Formats raw JSON payload into user-friendly property details table."""
    bed_count = int(payload["bedRoom"])
    bath_count = int(payload["bathroom"])

    details = [
        {"Property Attribute": "Property Type", "Details": str(payload["property_type"]).capitalize()},
        {"Property Attribute": "Sector", "Details": str(payload["sector"]).title()},
        {"Property Attribute": "Bedrooms", "Details": f"{bed_count} Bedroom" if bed_count == 1 else f"{bed_count} Bedrooms"},
        {"Property Attribute": "Bathrooms", "Details": f"{bath_count} Bathroom" if bath_count == 1 else f"{bath_count} Bathrooms"},
        {"Property Attribute": "Balcony", "Details": str(payload["balcony"])},
        {"Property Attribute": "Property Age", "Details": str(payload["agePossession"]).title()},
        {"Property Attribute": "Built-up Area", "Details": f"{payload['built_up_area']:,.0f} sq.ft"},
        {"Property Attribute": "Servant Room", "Details": "Available" if payload["servant_room"] == 1.0 else "Not Available"},
        {"Property Attribute": "Store Room", "Details": "Available" if payload["store_room"] == 1.0 else "Not Available"},
        {"Property Attribute": "Furnishing Type", "Details": str(payload["furnishing_type"]).title()},
        {"Property Attribute": "Luxury Category", "Details": str(payload["luxury_category"]).title()},
        {"Property Attribute": "Floor Category", "Details": str(payload["floor_category"]).title()},
    ]
    return pd.DataFrame(details)


# Prediction Action
if st.button("Predict Price", type="primary", use_container_width=True):
    payload = {
        "property_type": property_type,
        "sector": sector,
        "bedRoom": bedrooms,
        "bathroom": bathrooms,
        "balcony": balcony,
        "agePossession": property_age,
        "built_up_area": built_up_area,
        "servant_room": servant_room,
        "store_room": store_room,
        "furnishing_type": furnishing_type,
        "luxury_category": luxury_category,
        "floor_category": floor_category
    }

    with st.spinner("Requesting price prediction from FastAPI backend..."):
        try:
            res = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
            if res.status_code == 200:
                result = res.json()
                low = result["price_range_low_cr"]
                high = result["price_range_high_cr"]
                base = result["predicted_price_cr"]

                st.divider()
                st.subheader("🎯 Property Price Prediction Results")

                # 1. Estimated Price Range
                st.info(f"📊 **Estimated Price Range:** ₹ {low:.2f} Cr – ₹ {high:.2f} Cr")

                # 2. Predicted Base Price (Prominent Metric)
                st.metric(
                    label="Predicted Base Price",
                    value=f"₹ {base:.2f} Cr",
                    delta="Estimated Valuation"
                )

                st.markdown("<br>", unsafe_allow_html=True)

                # 3. Property Details Section & Responsive Table
                st.subheader("📋 PROPERTY DETAILS")
                details_df = format_property_details(payload)
                st.dataframe(
                    details_df,
                    use_container_width=True,
                    hide_index=True
                )

                # 4. Optional Collapsed API Debug Section
                with st.expander("🛠️ View API Payload & Response (Developer Debug)"):
                    st.json({
                        "endpoint": "POST /predict",
                        "request_payload": payload,
                        "fastapi_response": result
                    })

            else:
                err_detail = res.json().get("message", res.text)
                st.error(f"❌ API Error ({res.status_code}): {err_detail}")
        except Exception as e:
            st.error(f"❌ Failed to reach FastAPI backend: {str(e)}")