import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Price Prediction")

# Load dataframe
with open("data/df.pkl", "rb") as file:
    df = pickle.load(file)

# Load prediction pipeline
with open("data/pipeline.pkl", "rb") as file:
    pipeline = pickle.load(file)

st.header("Enter your inputs")

# Property type
property_type = st.selectbox(
    "Property Type",
    ["flat", "house"]
)

# Sector
sector = st.selectbox(
    "Sector",
    sorted(df["sector"].unique().tolist())
)

# Bedrooms
bedrooms = float(
    st.selectbox(
        "Number of Bedrooms",
        sorted(df["bedRoom"].unique().tolist())
    )
)

# Bathrooms
bathrooms = float(
    st.selectbox(
        "Number of Bathrooms",
        sorted(df["bathroom"].unique().tolist())
    )
)

# Balcony
balcony = st.selectbox(
    "Number of Balconies",
    sorted(df["balcony"].unique().tolist())
)

# Property age
property_age = st.selectbox(
    "Property Age",
    sorted(df["agePossession"].unique().tolist())
)

# Built-up area
built_up_area = float(
    st.number_input("Built-up Area in sqft")
)

# Servant room
servant_room = float(
    st.selectbox(
        "Servant Room",
        [0.0, 1.0]
    )
)

# Store room
store_room = float(
    st.selectbox(
        "Store Room",
        [0.0, 1.0]
    )
)

# Furnishing type
furnishing_type = st.selectbox(
    "Furnishing Type",
    sorted(df["furnishing_type"].unique().tolist())
)

# Luxury category
luxury_category = st.selectbox(
    "Luxury Category",
    sorted(df["luxury_category"].unique().tolist())
)

# Floor category
floor_category = st.selectbox(
    "Floor Category",
    sorted(df["floor_category"].unique().tolist())
)

# Prediction
if st.button("Predict Price"):

    data = [[
        property_type,
        sector,
        bedrooms,
        bathrooms,
        balcony,
        property_age,
        built_up_area,
        servant_room,
        store_room,
        furnishing_type,
        luxury_category,
        floor_category
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

    one_df = pd.DataFrame(data, columns=columns)

    st.dataframe(one_df)

    # Predict price
    base_price = (np.expm1(pipeline.predict(one_df)))[0]

    low = base_price - 0.22
    high = base_price + 0.22

    st.success(
        "The price of the property is between "
        f"{round(low, 2)} Cr and {round(high, 2)} Cr"
    )