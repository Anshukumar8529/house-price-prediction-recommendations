import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = os.getenv("API_URL", os.getenv("BACKEND_URL", "http://127.0.0.1:8000")).rstrip("/")

st.set_page_config(
    page_title="Real Estate Intelligence Platform",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom SaaS Dark Theme CSS System
st.markdown("""
<style>
    /* Main Layout & Dark Surface Theme */
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1240px;
    }

    /* Hide default Streamlit header bar decoration */
    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }
    .sidebar-brand {
        font-size: 1.1rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        color: #f59e0b;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }
    .sidebar-caption {
        font-size: 0.78rem;
        color: #9ca3af;
        margin-bottom: 1.5rem;
    }

    /* Hero Section Styling */
    .hero-eyebrow {
        text-transform: uppercase;
        letter-spacing: 0.15em;
        font-size: 0.8rem;
        font-weight: 700;
        color: #f59e0b;
        margin-bottom: 0.75rem;
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        line-height: 1.15;
        color: #ffffff;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #9ca3af;
        line-height: 1.6;
        margin-bottom: 2rem;
        max-width: 540px;
    }

    /* Hero Right Visual Property Display */
    .hero-visual-card {
        background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.75rem;
        position: relative;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }
    .hero-badge-float {
        display: inline-block;
        background-color: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .hero-property-price {
        font-size: 2.2rem;
        font-weight: 800;
        color: #10b981;
        letter-spacing: -0.01em;
    }
    .hero-property-location {
        font-size: 1rem;
        font-weight: 600;
        color: #f3f4f6;
        margin-bottom: 0.5rem;
    }
    .hero-property-specs {
        font-size: 0.875rem;
        color: #9ca3af;
        border-top: 1px solid #334155;
        padding-top: 0.75rem;
        margin-top: 0.75rem;
    }

    /* Horizontal Metrics Strip */
    .metrics-strip {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 10px;
        padding: 1.25rem 2rem;
        display: flex;
        justify-content: space-around;
        align-items: center;
        margin-top: 2rem;
        margin-bottom: 3.5rem;
    }
    .metric-item {
        text-align: center;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #ffffff;
    }
    .metric-label {
        font-size: 0.82rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.2rem;
    }
    .metric-divider {
        width: 1px;
        height: 35px;
        background-color: #374151;
    }

    /* Section Headers */
    .section-header-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.01em;
        margin-bottom: 0.35rem;
    }
    .section-header-sub {
        font-size: 0.9rem;
        color: #9ca3af;
        margin-bottom: 1.5rem;
    }

    /* Product Action Panel Styling */
    .product-panel {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 10px;
        padding: 1.5rem;
        height: 100%;
        transition: border-color 0.2s ease, transform 0.2s ease;
    }
    .product-panel:hover {
        border-color: #f59e0b;
        transform: translateY(-2px);
    }
    .panel-num {
        font-size: 0.8rem;
        font-weight: 700;
        color: #f59e0b;
        margin-bottom: 0.75rem;
    }
    .panel-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    .panel-desc {
        font-size: 0.875rem;
        color: #9ca3af;
        line-height: 1.5;
        margin-bottom: 1.25rem;
    }

    /* Insight Card Styling */
    .insight-card {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 10px;
        padding: 1.5rem;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .insight-tag {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        color: #f59e0b;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .insight-text {
        font-size: 1.05rem;
        color: #e5e7eb;
        line-height: 1.5;
        margin-bottom: 1rem;
    }
    .insight-highlight {
        font-size: 2.2rem;
        font-weight: 800;
        color: #10b981;
    }

    /* Property Listing Preview Card */
    .listing-card {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 10px;
        padding: 1.25rem;
        transition: border-color 0.2s ease;
    }
    .listing-card:hover {
        border-color: #374151;
    }
    .listing-sector {
        font-size: 1.05rem;
        font-weight: 700;
        color: #ffffff;
    }
    .listing-type {
        font-size: 0.8rem;
        color: #f59e0b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.15rem;
    }
    .listing-specs {
        font-size: 0.875rem;
        color: #9ca3af;
        margin-top: 0.75rem;
    }
    .listing-price {
        font-size: 1.25rem;
        font-weight: 800;
        color: #10b981;
        margin-top: 0.75rem;
    }

    /* How It Works Journey Step */
    .journey-step {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 8px;
        padding: 1.25rem;
        height: 100%;
    }
    .journey-num {
        font-size: 0.85rem;
        font-weight: 800;
        color: #f59e0b;
        margin-bottom: 0.5rem;
    }
    .journey-title {
        font-size: 1rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.35rem;
    }
    .journey-desc {
        font-size: 0.825rem;
        color: #9ca3af;
        line-height: 1.45;
    }

    /* Tech Trust Bar & Footer */
    .tech-bar {
        text-align: center;
        padding: 1.5rem 0;
        border-top: 1px solid #1f2937;
        margin-top: 3.5rem;
        font-size: 0.825rem;
        color: #6b7280;
    }
    .tech-item {
        color: #9ca3af;
        font-weight: 600;
        margin: 0 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# Sidebar Navigation & Info
with st.sidebar:
    st.markdown('<div class="sidebar-brand">REAL ESTATE</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-caption">INTELLIGENCE PLATFORM</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("Home.py", label="Home", icon="🏠")
    st.page_link("pages/Price Prediction.py", label="Price Prediction", icon="📈")
    st.page_link("pages/Recommend Apartments.py", label="Property Discovery", icon="🏢")
    st.page_link("pages/Analytics.py", label="Market Analytics", icon="📊")
    st.markdown("---")
    st.caption("ML-Powered Property Intelligence")


# Load Dataset Analytics & Metrics safely
@st.cache_data(ttl=600)
def load_market_metrics():
    try:
        res = requests.get(f"{API_URL}/analytics", timeout=3)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    
    try:
        df = pd.read_csv("data/data_viz1.csv")
        return {
            "total_properties": int(len(df)),
            "avg_price": float(round(df["price"].mean(), 2)),
            "sector_count": int(df["sector"].nunique()),
            "avg_price_per_sqft": float(round(df["price_per_sqft"].mean(), 2))
        }
    except Exception:
        return {
            "total_properties": 3294,
            "avg_price": 2.55,
            "sector_count": 105,
            "avg_price_per_sqft": 13850
        }

metrics = load_market_metrics()


# ---------------------------------------------------------------------------
# 1. HERO SECTION (2-Column Layout)
# ---------------------------------------------------------------------------
hero_left, hero_right = st.columns([1.35, 1])

with hero_left:
    st.markdown('<div class="hero-eyebrow">REAL ESTATE INTELLIGENCE PLATFORM</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-title">Know the Value.<br>Find the Right Property.</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="hero-subtitle">'
        'Predict property prices, discover similar homes, and explore real-estate market insights using machine learning.'
        '</div>',
        unsafe_allow_html=True
    )

    cta_col1, cta_col2, cta_spacer = st.columns([1.2, 1.2, 1])
    with cta_col1:
        st.page_link("pages/Price Prediction.py", label="Predict Property Price", use_container_width=True)
    with cta_col2:
        st.page_link("pages/Recommend Apartments.py", label="Explore Properties", use_container_width=True)

with hero_right:
    st.markdown("""
    <div class="hero-visual-card">
        <div class="hero-badge-float">FEATURED MARKET INDEX</div>
        <div class="hero-property-price">₹ 2.55 Cr</div>
        <div class="hero-property-location">Sector 102, Gurgaon</div>
        <div style="color: #9ca3af; font-size: 0.9rem;">High Demand Premium Residential Hub</div>
        <div class="hero-property-specs">
            4 BHK &nbsp;•&nbsp; 2,225 sq.ft &nbsp;•&nbsp; Valued via Scikit-Learn ML
        </div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 2. COMPACT HORIZONTAL METRICS STRIP
# ---------------------------------------------------------------------------
st.markdown(f"""
<div class="metrics-strip">
    <div class="metric-item">
        <div class="metric-value">{metrics.get("total_properties", 3294):,}</div>
        <div class="metric-label">Properties Analyzed</div>
    </div>
    <div class="metric-divider"></div>
    <div class="metric-item">
        <div class="metric-value">₹ {metrics.get("avg_price", 2.55):.2f} Cr</div>
        <div class="metric-label">Average Property Price</div>
    </div>
    <div class="metric-divider"></div>
    <div class="metric-item">
        <div class="metric-value">{metrics.get("sector_count", 105)} Locations</div>
        <div class="metric-label">Covered</div>
    </div>
    <div class="metric-divider"></div>
    <div class="metric-item">
        <div class="metric-value">₹ {metrics.get("avg_price_per_sqft", 13850):,.0f}</div>
        <div class="metric-label">Avg Price / Sq.ft</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 3. WHAT CAN YOU DO? (EXPLORE THE PLATFORM)
# ---------------------------------------------------------------------------
st.markdown('<div class="section-header-title">Explore the Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header-sub">Select an intelligence tool to start evaluating real estate data</div>', unsafe_allow_html=True)

p1, p2, p3 = st.columns(3)

with p1:
    st.markdown("""
    <div class="product-panel">
        <div class="panel-num">01</div>
        <div class="panel-title">PRICE PREDICTION</div>
        <div class="panel-desc">Estimate the market value of any property based on location, area, rooms, furnishing, and luxury attributes.</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/Price Prediction.py", label="Predict Price →", use_container_width=True)

with p2:
    st.markdown("""
    <div class="product-panel">
        <div class="panel-num">02</div>
        <div class="panel-title">PROPERTY DISCOVERY</div>
        <div class="panel-desc">Find properties that match your preferences using weighted cosine similarity recommendation algorithms.</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/Recommend Apartments.py", label="Explore Properties →", use_container_width=True)

with p3:
    st.markdown("""
    <div class="product-panel">
        <div class="panel-num">03</div>
        <div class="panel-title">MARKET ANALYTICS</div>
        <div class="panel-desc">Understand prices, spatial sector geomaps, BHK distributions, and key real estate market patterns.</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/Analytics.py", label="View Market →", use_container_width=True)


st.markdown("<br><br>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 4. REAL ESTATE MARKET INSIGHT SECTION (Chart + Dynamic Insight)
# ---------------------------------------------------------------------------
st.markdown('<div class="section-header-title">Market Insights</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header-sub">Real-time valuation trends across bedroom configurations</div>', unsafe_allow_html=True)

chart_col, insight_col = st.columns([1.6, 1])

# Dynamic calculation from dataset
max_bhk_num = 6
max_bhk_val = 7.98

try:
    df_viz = pd.read_csv("data/data_viz1.csv")
    bhk_means = df_viz[df_viz["bedRoom"] <= 6].groupby("bedRoom")["price"].mean()
    max_bhk_num = int(bhk_means.idxmax())
    max_bhk_val = float(bhk_means.max())
except Exception:
    pass

with chart_col:
    try:
        df_viz = pd.read_csv("data/data_viz1.csv")
        bhk_df = df_viz[df_viz["bedRoom"] <= 6].groupby("bedRoom")["price"].mean().reset_index()
        bhk_df["bedRoom"] = bhk_df["bedRoom"].astype(int).astype(str) + " BHK"

        fig_bhk = px.bar(
            bhk_df,
            x="bedRoom",
            y="price",
            text_auto=".2f",
            color_discrete_sequence=["#f59e0b"]
        )
        fig_bhk.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=300,
            xaxis_title=None,
            yaxis_title="Average Price (Crores)",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#9ca3af")
        )
        fig_bhk.update_traces(marker_line_color="#1e293b", marker_line_width=1)
        st.plotly_chart(fig_bhk, use_container_width=True)
    except Exception:
        st.info("Market chart loading...")

with insight_col:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-tag">VALUATION INSIGHT</div>
        <div class="insight-text">
            <strong>{max_bhk_num} BHK</strong> properties demonstrate the highest average valuation across all sectors in the dataset.
        </div>
        <div class="insight-highlight">₹ {max_bhk_val:.2f} Cr</div>
        <div style="font-size: 0.8rem; color: #6b7280; margin-top: 0.5rem;">Calculated dynamically from dataset records</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<br><br>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 5. PROPERTY DISCOVERY PREVIEW
# ---------------------------------------------------------------------------
st.markdown('<div class="section-header-title">Property Discovery</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header-sub">Explore properties from the current market dataset</div>', unsafe_allow_html=True)

try:
    df_sample = pd.read_csv("data/data_viz1.csv").head(3)
    l1, l2, l3 = st.columns(3)

    for lcol, (_, r) in zip([l1, l2, l3], df_sample.iterrows()):
        with lcol:
            st.markdown(f"""
            <div class="listing-card">
                <div class="listing-sector">{str(r['sector']).title()}</div>
                <div class="listing-type">{str(r['property_type']).upper()}</div>
                <div class="listing-specs">{int(r['bedRoom'])} BHK &nbsp;•&nbsp; {r['built_up_area']:,.0f} sq.ft</div>
                <div class="listing-price">₹ {r['price']:.2f} Cr</div>
            </div>
            """, unsafe_allow_html=True)
            st.page_link("pages/Recommend Apartments.py", label="View Property →", use_container_width=True)
except Exception:
    pass


st.markdown("<br><br>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 6. HOW IT WORKS (Visual Horizontal Journey)
# ---------------------------------------------------------------------------
st.markdown('<div class="section-header-title">How It Works</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header-sub">End-to-end evaluation and discovery workflow</div>', unsafe_allow_html=True)

j1, j2, j3, j4 = st.columns(4)

with j1:
    st.markdown("""
    <div class="journey-step">
        <div class="journey-num">01</div>
        <div class="journey-title">PROPERTY DETAILS</div>
        <div class="journey-desc">Enter location, built-up area, rooms, and luxury level attributes.</div>
    </div>
    """, unsafe_allow_html=True)

with j2:
    st.markdown("""
    <div class="journey-step">
        <div class="journey-num">02</div>
        <div class="journey-title">FASTAPI + ML</div>
        <div class="journey-desc">FastAPI validates inputs & executes the pre-trained Scikit-Learn pipeline.</div>
    </div>
    """, unsafe_allow_html=True)

with j3:
    st.markdown("""
    <div class="journey-step">
        <div class="journey-num">03</div>
        <div class="journey-title">PRICE ESTIMATE</div>
        <div class="journey-desc">Receive the estimated base price and interval confidence range.</div>
    </div>
    """, unsafe_allow_html=True)

with j4:
    st.markdown("""
    <div class="journey-step">
        <div class="journey-num">04</div>
        <div class="journey-title">DISCOVER</div>
        <div class="journey-desc">Explore similar properties using recommendation matrices and market insights.</div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 7. TECHNOLOGY TRUST BAR & FOOTER
# ---------------------------------------------------------------------------
st.markdown("""
<div class="tech-bar">
    <span>Built with</span>
    <span class="tech-item">Python</span> &bull;
    <span class="tech-item">Scikit-Learn</span> &bull;
    <span class="tech-item">FastAPI</span> &bull;
    <span class="tech-item">Streamlit</span> &bull;
    <span class="tech-item">Pandas</span>
</div>
""", unsafe_allow_html=True)