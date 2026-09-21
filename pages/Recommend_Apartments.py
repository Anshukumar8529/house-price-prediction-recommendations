import os
import streamlit as st
import requests
import pandas as pd

API_URL = os.getenv("API_URL", os.getenv("BACKEND_URL", "http://127.0.0.1:8000")).rstrip("/")

st.set_page_config(page_title="Recommend Apartments", page_icon="🏢")

st.title("🏢 Property & Location Recommender")
st.markdown("*(Powered by FastAPI Backend & Cosine Similarity Matrix)*")


@st.cache_data(ttl=600)
def get_options():
    try:
        res = requests.get(f"{API_URL}/options", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        st.error(f"⚠️ Could not connect to FastAPI server at `{API_URL}`. Please start uvicorn backend.")
        st.info("Run: `uvicorn backend.main:app --reload`")
        return None
    return None

options = get_options()

if options is None:
    st.stop()

# ---------------------------------------------------------------------------
# 1. Location and Radius Search Section
# ---------------------------------------------------------------------------
st.header("1. Search Locations within Radius")

col1, col2 = st.columns(2)
with col1:
    selected_location = st.selectbox(
        "Select Target Location/Sector",
        options.get("locations", [])
    )
with col2:
    radius = st.number_input(
        "Radius in kms",
        min_value=0.1,
        value=5.0,
        step=0.5
    )

if st.button("Search Radius"):
    payload = {
        "location": selected_location,
        "radius_km": float(radius)
    }

    with st.spinner("Fetching nearby locations from FastAPI (`POST /recommend/radius`)..."):
        try:
            res = requests.post(f"{API_URL}/recommend/radius", json=payload, timeout=10)
            if res.status_code == 200:
                data = res.json().get("results", [])
                if data:
                    res_df = pd.DataFrame(data)
                    res_df.columns = ["Location / Sector", "Distance (km)"]
                    st.dataframe(res_df, use_container_width=True)
                else:
                    st.info("No nearby locations found within this radius.")
            else:
                st.error(f"API Error ({res.status_code}): {res.json().get('message', res.text)}")
        except Exception as e:
            st.error(f"Failed to communicate with FastAPI API: {str(e)}")


st.divider()

# ---------------------------------------------------------------------------
# 2. Apartment Recommendation Section
# ---------------------------------------------------------------------------
st.header("2. Recommend Similar Apartments")

selected_apartment = st.selectbox(
    "Select an Apartment",
    options.get("apartment_names", [])
)

top_n = st.slider("Number of Recommendations", min_value=1, max_value=15, value=5)

if st.button("Get Recommendations", type="primary"):
    payload = {
        "property_name": selected_apartment,
        "top_n": top_n
    }

    with st.spinner("Calculating recommendations via FastAPI (`POST /recommend`)..."):
        try:
            res = requests.post(f"{API_URL}/recommend", json=payload, timeout=10)
            if res.status_code == 200:
                recs = res.json().get("recommendations", [])
                if recs:
                    rec_df = pd.DataFrame(recs)
                    rec_df.columns = ["Recommended Property", "Similarity Score"]
                    st.success(f"Top {len(recs)} recommended properties for **{selected_apartment}**:")
                    st.dataframe(rec_df, use_container_width=True)
                else:
                    st.warning("No recommendations returned.")
            else:
                st.error(f"API Error ({res.status_code}): {res.json().get('message', res.text)}")
        except Exception as e:
            st.error(f"Failed to fetch recommendations: {str(e)}")