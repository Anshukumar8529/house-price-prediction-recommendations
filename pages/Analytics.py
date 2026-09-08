import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
import pickle
import seaborn as sns

st.set_page_config(page_title="Analytics")

st.title("Analytics")

st.header("Sector Price per Sqft Geomap")

# Load visualization dataset
new_df = pd.read_csv("data/data_viz1.csv")

group_df = new_df.groupby("sector")[
    ["price", "price_per_sqft", "built_up_area", "latitude", "longitude"]
].mean()

fig = px.scatter_mapbox(
    group_df,
    lat="latitude",
    lon="longitude",
    size="built_up_area",
    color="price_per_sqft",
    color_continuous_scale=px.colors.cyclical.IceFire,
    zoom=10,
    mapbox_style="open-street-map",
    width=1200,
    height=800,
    hover_name=group_df.index
)

st.plotly_chart(fig, use_container_width=True)

# Load pickle file for wordcloud
st.header("Feature Wordcloud")

with open("data/sector_wordcloud.pkl", "rb") as f:
    sector_features = pickle.load(f)

selected_sector = st.selectbox(
    "Select Sector",
    sorted(sector_features.keys())
)

text = sector_features[selected_sector]

# Word Cloud
wordcloud = WordCloud(
    width=800,
    height=800,
    background_color="white"
).generate(text)

fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")

st.pyplot(fig)

# Area vs Price
st.header("Area vs Price")

property_type = st.selectbox(
    "Select Property Type",
    ["flat", "house"]
)

if property_type == "house":
    fig1 = px.scatter(
        new_df[new_df["property_type"] == "house"],
        x="built_up_area",
        y="price",
        color="bedRoom",
        title="Area vs Price"
    )
else:
    fig1 = px.scatter(
        new_df[new_df["property_type"] == "flat"],
        x="built_up_area",
        y="price",
        color="bedRoom",
        title="Area vs Price"
    )

st.plotly_chart(fig1, use_container_width=True)

# BHK Pie Chart
st.header("BHK Pie Chart")

sector_options = new_df["sector"].unique().tolist()
sector_options.insert(0, "All Sectors")

selected_sector = st.selectbox(
    "Select Sector",
    sector_options
)

if selected_sector == "All Sectors":
    fig2 = px.pie(
        new_df,
        names="bedRoom"
    )
else:
    fig2 = px.pie(
        new_df[new_df["sector"] == selected_sector],
        names="bedRoom"
    )

st.plotly_chart(fig2, use_container_width=True)

# BHK Price Comparison
st.header("Side by Side BHK Price Comparison")

fig3 = px.box(
    new_df[new_df["bedRoom"] <= 4],
    x="bedRoom",
    y="price",
    title="BHK Price Range"
)

st.plotly_chart(fig3, use_container_width=True)

# Property Type Distribution
st.header("Side By Side Displot for Property Type")

fig4 = sns.displot(
    data=new_df,
    x="price",
    hue="property_type",
    kind="kde",
    fill=True,
    height=5,
    aspect=2
)

fig4.set_axis_labels("Price (Crores)", "Density")

st.pyplot(fig4.figure)