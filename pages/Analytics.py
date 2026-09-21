import os
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
import seaborn as sns

API_URL = os.getenv("API_URL", os.getenv("BACKEND_URL", "http://127.0.0.1:8000")).rstrip("/")

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

st.title("📊 Real Estate Market Analytics")
st.markdown("*(Powered by FastAPI Analytics Service)*")

# Fetch analytics summary from FastAPI
@st.cache_data(ttl=600)
def get_analytics_summary():
    try:
        res = requests.get(f"{API_URL}/analytics", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        return None
    return None

summary = get_analytics_summary()

if summary:
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Properties", f"{summary.get('total_properties', 0):,}")
    col2.metric("Avg Price", f"₹ {summary.get('avg_price', 0):.2f} Cr")
    col3.metric("Min Price", f"₹ {summary.get('min_price', 0):.2f} Cr")
    col4.metric("Max Price", f"₹ {summary.get('max_price', 0):.2f} Cr")
    col5.metric("Avg Price/Sqft", f"₹ {summary.get('avg_price_per_sqft', 0):,.0f}")

st.divider()

# Load visualization dataset from data_viz1.csv for interactive Plotly/Seaborn renders
@st.cache_data
def load_viz_data():
    return pd.read_csv("data/data_viz1.csv")

new_df = load_viz_data()

# ---------------------------------------------------------------------------
# Sector Price per Sqft Geomap
# ---------------------------------------------------------------------------
st.header("1. Sector Price per Sqft Geomap")

group_df = new_df.groupby("sector")[
    ["price", "price_per_sqft", "built_up_area", "latitude", "longitude"]
].mean().reset_index()

fig_map = px.scatter_mapbox(
    group_df,
    lat="latitude",
    lon="longitude",
    size="built_up_area",
    color="price_per_sqft",
    color_continuous_scale=px.colors.cyclical.IceFire,
    zoom=10,
    mapbox_style="open-street-map",
    width=1200,
    height=600,
    hover_name="sector"
)

st.plotly_chart(fig_map, use_container_width=True)


# ---------------------------------------------------------------------------
# Feature Wordcloud (via FastAPI GET /analytics/wordcloud/{sector})
# ---------------------------------------------------------------------------
st.header("2. Sector Feature Wordcloud")

@st.cache_data(ttl=600)
def get_wordcloud_sectors():
    try:
        res = requests.get(f"{API_URL}/analytics/wordcloud-sectors", timeout=5)
        if res.status_code == 200:
            return res.json().get("sectors", [])
    except Exception:
        pass
    return []

sectors_wc = get_wordcloud_sectors()

if sectors_wc:
    selected_sector = st.selectbox("Select Sector for Wordcloud", sectors_wc)

    if st.button("Generate Wordcloud"):
        with st.spinner("Fetching sector text from FastAPI..."):
            try:
                res = requests.get(f"{API_URL}/analytics/wordcloud/{selected_sector}", timeout=5)
                if res.status_code == 200:
                    text = res.json().get("text", "")
                    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
                    fig_wc, ax = plt.subplots(figsize=(10, 5))
                    ax.imshow(wordcloud, interpolation="bilinear")
                    ax.axis("off")
                    st.pyplot(fig_wc)
                else:
                    st.error("Failed to fetch wordcloud text.")
            except Exception as e:
                st.error(f"Error: {str(e)}")


st.divider()

# ---------------------------------------------------------------------------
# Area vs Price
# ---------------------------------------------------------------------------
st.header("3. Area vs Price")

property_type = st.selectbox("Select Property Type", ["flat", "house"])

fig_scatter = px.scatter(
    new_df[new_df["property_type"] == property_type],
    x="built_up_area",
    y="price",
    color="bedRoom",
    title=f"Built-up Area vs Price ({property_type.capitalize()})"
)
st.plotly_chart(fig_scatter, use_container_width=True)


# ---------------------------------------------------------------------------
# BHK Pie Chart
# ---------------------------------------------------------------------------
st.header("4. BHK Pie Chart")

sector_options = new_df["sector"].unique().tolist()
sector_options.insert(0, "All Sectors")

selected_sector_bhk = st.selectbox("Select Sector for BHK Breakdown", sector_options)

if selected_sector_bhk == "All Sectors":
    fig_pie = px.pie(new_df, names="bedRoom", title="BHK Distribution across All Sectors")
else:
    fig_pie = px.pie(
        new_df[new_df["sector"] == selected_sector_bhk],
        names="bedRoom",
        title=f"BHK Distribution in {selected_sector_bhk}"
    )

st.plotly_chart(fig_pie, use_container_width=True)


# ---------------------------------------------------------------------------
# BHK Price Comparison
# ---------------------------------------------------------------------------
st.header("5. Side by Side BHK Price Comparison")

fig_box = px.box(
    new_df[new_df["bedRoom"] <= 4],
    x="bedRoom",
    y="price",
    title="BHK Price Range Boxplot"
)
st.plotly_chart(fig_box, use_container_width=True)


# ---------------------------------------------------------------------------
# Property Type Distribution
# ---------------------------------------------------------------------------
st.header("6. Displot for Property Type Distribution")

fig_kde = sns.displot(
    data=new_df,
    x="price",
    hue="property_type",
    kind="kde",
    fill=True,
    height=5,
    aspect=2
)
fig_kde.set_axis_labels("Price (Crores)", "Density")
st.pyplot(fig_kde.figure)