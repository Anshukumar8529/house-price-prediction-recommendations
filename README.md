# House Price Prediction & Apartment Recommendation

This is an end-to-end data science project based on real estate data.

The project has a Streamlit web application where you can:

- Predict the price of a property
- Explore different real estate analytics
- Search properties based on location and radius
- Get apartment recommendations based on similarity

## Live Demo

https://house-price-prediction-recommendations.onrender.com

## GitHub Repository

https://github.com/Anshukumar8529/house-price-prediction-recommendations

## About the Project

The main idea of this project was to build a complete real estate application starting from data preprocessing and analysis to machine learning and deployment.

I worked on the data cleaning, exploratory analysis, feature engineering, feature selection, model building and recommendation system before integrating everything into a Streamlit application.

The final application contains three main sections:

### 1. Price Prediction

The price prediction page takes different property details as input, such as:

- Property type
- Sector
- Bedrooms
- Bathrooms
- Balconies
- Property age
- Built-up area
- Servant room
- Store room
- Furnishing type
- Luxury category
- Floor category

Based on these inputs, the trained model predicts the approximate property price.

The trained pipeline is stored in:

```text
data/pipeline.pkl