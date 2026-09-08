import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Recommend Apartments")

# Load recommendation data
with open("data/location_distance.pkl", "rb") as file:
    location_df = pickle.load(file)

with open("data/cosine_sim1.pkl", "rb") as file:
    cosine_sim1 = pickle.load(file)

with open("data/cosine_sim2.pkl", "rb") as file:
    cosine_sim2 = pickle.load(file)

with open("data/cosine_sim3.pkl", "rb") as file:
    cosine_sim3 = pickle.load(file)


def recommend_properties_with_scores(property_name, top_n=5):

    cosine_sim_matrix = (
        30 * cosine_sim1
        + 20 * cosine_sim2
        + 8 * cosine_sim3
    )

    sim_scores = list(
        enumerate(
            cosine_sim_matrix[
                location_df.index.get_loc(property_name)
            ]
        )
    )

    sorted_scores = sorted(
        sim_scores,
        key=lambda x: x[1],
        reverse=True
    )

    top_indices = [
        i[0]
        for i in sorted_scores[1:top_n + 1]
    ]

    top_scores = [
        i[1]
        for i in sorted_scores[1:top_n + 1]
    ]

    top_properties = location_df.index[
        top_indices
    ].tolist()

    recommendations_df = pd.DataFrame({
        "PropertyName": top_properties,
        "SimilarityScore": top_scores
    })

    return recommendations_df


# Location and Radius Search
st.title("Select Location and Radius")

selected_location = st.selectbox(
    "Select Location",
    sorted(location_df.columns.to_list())
)

radius = st.number_input(
    "Radius in kms",
    min_value=0.0
)

if st.button("Search"):

    result_ser = (
        location_df[
            location_df[selected_location] < radius * 1000
        ][selected_location]
        .sort_values()
    )

    for key, value in result_ser.items():
        st.write(
            f"{key} : {value / 1000:.2f} kms"
        )


# Apartment Recommendation
st.title("Recommend Apartments")

selected_apartment = st.selectbox(
    "Select an Apartment",
    sorted(location_df.index.to_list())
)

if st.button("Recommend"):

    recommendation_df = recommend_properties_with_scores(
        selected_apartment
    )

    st.dataframe(
        recommendation_df,
        use_container_width=True
    )