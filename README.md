# 🏠 Real Estate House Price Prediction & Recommendation System

Production-grade Machine Learning application upgraded with a **FastAPI REST API** backend and **Streamlit** frontend interface.

---

## 📐 Architecture Overview

```
                          ┌───────────────────────────┐
                          │   Streamlit Frontend UI   │
                          │   (Home, Predict, Recs)   │
                          └─────────────┬─────────────┘
                                        │
                               HTTP POST / GET (JSON)
                                        │
                          ┌─────────────▼─────────────┐
                          │    FastAPI REST Backend   │
                          │     (Uvicorn WebServer)   │
                          └─────────────┬─────────────┘
                                        │
                             Pydantic Validation
                                        │
              ┌─────────────────────────┼─────────────────────────┐
              │                         │                         │
    ┌─────────▼─────────┐     ┌─────────▼─────────┐     ┌─────────▼─────────┐
    │  Model Service    │     │  Recommendation   │     │Analytics Service  │
    │  (pipeline.pkl)   │     │ (cosine_sim*.pkl) │     │ (data_viz1.csv)   │
    └───────────────────┘     └───────────────────┘     └───────────────────┘
```

---

## 📁 Project Structure

```
house-price-prediction/
│
├── backend/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application & REST routes
│   ├── schemas.py               # Pydantic request/response validation schemas
│   ├── model_service.py         # ML pipeline loader & price prediction engine
│   ├── recommendation_service.py # Cosine similarity & radius search engine
│   └── analytics_service.py     # Real estate market analytics service
│
├── data/
│   ├── pipeline.pkl             # Trained Scikit-Learn prediction pipeline
│   ├── df.pkl                   # Cleaned dataset pickle for dropdown options
│   ├── location_distance.pkl    # Location coordinate & distance matrix
│   ├── cosine_sim1.pkl          # Cosine similarity matrix 1
│   ├── cosine_sim2.pkl          # Cosine similarity matrix 2
│   ├── cosine_sim3.pkl          # Cosine similarity matrix 3
│   ├── data_viz1.csv            # Geospatial & visualization dataset
│   └── sector_wordcloud.pkl     # Sector feature text data
│
├── pages/
│   ├── Price Prediction.py      # Streamlit UI for price estimation
│   ├── Recommend Apartments.py  # Streamlit UI for apartment & location recommendations
│   └── Analytics.py             # Streamlit UI for market visualizations
│
├── Home.py                      # Main Streamlit entrance page
├── requirements.txt             # Python dependencies
├── .env.example                 # Sample environment variables
└── README.md                    # Project documentation
```

---

## ⚡ Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch FastAPI Backend Server
```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```
- Swagger Interactive Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc Documentation: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### 3. Launch Streamlit Frontend Application
```bash
streamlit run Home.py
```

---

## 🔌 API Endpoints Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Server status check |
| `GET` | `/options` | Form dropdown options metadata |
| `POST` | `/predict` | Estimate property price via Scikit-Learn pipeline |
| `POST` | `/recommend` | Recommend similar properties using Cosine Similarity |
| `POST` | `/recommend/radius` | Search locations within kilometer radius |
| `GET` | `/analytics` | Market summary statistics |
| `GET` | `/analytics/wordcloud/{sector}` | Fetch wordcloud text for a specific sector |

---

## 🧪 Testing with cURL / JSON Examples

### 1. Health Check
```bash
curl -X GET "http://127.0.0.1:8000/health"
```

### 2. Predict Price (`POST /predict`)
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
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
     }'
```

---

## 🎓 Technology Stack

- **Backend**: FastAPI, Pydantic, Uvicorn, Python 3.12
- **Machine Learning**: Scikit-learn, Pandas, NumPy, Pickle
- **Frontend**: Streamlit, Plotly, Seaborn, Matplotlib, WordCloud