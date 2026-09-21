# Real Estate Price Prediction & Recommendation Engine

A full-stack machine learning web application that estimates real estate property valuations and provides content-based property recommendations. Built with a decoupled architecture featuring a **FastAPI** backend for ML inference and a **Streamlit** frontend for interactive analysis.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-blue?style=for-the-badge&logo=render)](https://real-estate-frontend-d8hn.onrender.com)
[![API Docs](https://img.shields.io/badge/API%20Docs-Swagger-green?style=for-the-badge&logo=fastapi)](https://real-estate-backend-7h1x.onrender.com/docs)

---

## 📌 Project Highlights

* **Decoupled Architecture**: Clean separation between machine learning microservices (FastAPI) and the user interface (Streamlit), allowing independent scaling and API integration.
* **Price Prediction Pipeline**: Scikit-Learn regression pipeline predicting property prices based on location, area, rooms, furnishing level, and luxury metrics.
* **Recommendation System**: Content-based filtering using precomputed Cosine Similarity matrices to recommend similar properties and location radius searches.
* **Geospatial & Market Analytics**: Interactive visualizations including price distribution by sector, sqft rate heatmaps, and BHK breakdown using Plotly & Seaborn.
* **Production Deployment**: Containerized with Docker and deployed to Render with automated multi-service orchestration via `render.yaml`.

---

## 📐 Architecture

```
                       ┌──────────────────────────────┐
                       │    Streamlit Frontend UI     │
                       │ (Home, Predict, Recs, Stats) │
                       └──────────────┬───────────────┘
                                      │
                             HTTP Requests (JSON)
                                      │
                       ┌──────────────▼───────────────┐
                       │     FastAPI REST Backend     │
                       │     (ASGI / Uvicorn Server)  │
                       └──────────────┬───────────────┘
                                      │
                           Pydantic Request Validation
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         │                            │                            │
┌────────▼─────────┐        ┌─────────▼─────────┐        ┌─────────▼─────────┐
│  Model Service   │        │ Recommendation Svc│        │ Analytics Service │
│ (scikit-learn)   │        │ (cosine similarity│        │ (pandas & plotly) │
└──────────────────┘        └───────────────────┘        └───────────────────┘
```

---

## 📁 Repository Layout

```text
├── backend/
│   ├── main.py                  # FastAPI application entrypoint & routing
│   ├── schemas.py               # Pydantic data validation schemas
│   ├── model_service.py         # ML model loading & prediction logic
│   ├── recommendation_service.py # Cosine similarity & location radius search
│   └── analytics_service.py     # Aggregations & dataset summary stats
│
├── pages/
│   ├── Price_Prediction.py      # Property valuation interface
│   ├── Recommend_Apartments.py  # Property recommendation & radius search UI
│   └── Analytics.py             # Market analytics dashboards
│
├── data/                        # Trained models, encoders & processed data
│   ├── pipeline.pkl             # Serialized Scikit-Learn model pipeline
│   ├── df.pkl                   # Cleaned property dataset
│   └── cosine_sim*.pkl          # Similarity matrices
│
├── Home.py                      # Streamlit application entrypoint
├── Dockerfile                   # Multi-stage production container
├── render.yaml                  # Infrastructure-as-code for Render deployment
└── requirements.txt             # Project dependencies
```

---

## 🛠️ Tech Stack

* **Backend**: Python 3.10+, FastAPI, Uvicorn, Pydantic
* **Machine Learning**: Scikit-Learn, Pandas, NumPy
* **Frontend**: Streamlit, Plotly, Seaborn, Matplotlib, WordCloud
* **DevOps**: Docker, Docker Compose, Render Blueprint

---

## 🚀 Local Development Setup

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/Anshukumar8529/house-price-prediction-recommendations.git
cd house-price-prediction-recommendations

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Start Backend API
```bash
python -m uvicorn backend.main:app --reload --port 8000
```
* API Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 3. Start Frontend UI
```bash
streamlit run Home.py
```
* Web Application: [http://localhost:8501](http://localhost:8501)

---

## 📡 API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/health` | `GET` | Health check endpoint |
| `/options` | `GET` | Fetches dynamic dropdown options for UI forms |
| `/predict` | `POST` | Calculates property price prediction |
| `/recommend` | `POST` | Returns top N similar property recommendations |
| `/recommend/radius` | `POST` | Performs geospatial radius search for sectors |
| `/analytics` | `GET` | Returns aggregated market statistics |

### Sample Prediction Request (`POST /predict`)
```json
{
  "property_type": "flat",
  "sector": "sector 102",
  "bedRoom": 3.0,
  "bathroom": 2.0,
  "balcony": "2",
  "agePossession": "Relatively New",
  "built_up_area": 1500.0,
  "servant_room": 0.0,
  "store_room": 0.0,
  "furnishing_type": "semifurnished",
  "luxury_category": "Medium",
  "floor_category": "Mid Floor"
}
```

---

## 🐳 Docker Execution

Run the complete multi-service application with Docker Compose:

```bash
docker-compose up -d --build
```

---

## 👤 Author

**Anshu Kumar**
- GitHub: [@Anshukumar8529](https://github.com/Anshukumar8529)