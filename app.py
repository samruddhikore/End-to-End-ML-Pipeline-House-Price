import streamlit as st
import pickle
import numpy as np

# Load trained model
with open("models/model.pkl", "rb") as file:
    model = pickle.load(file)

# Title
st.title("Simple House Price Prediction")
st.write("Enter house details below:")

# Inputs
area = st.number_input("Area (Square Feet)", min_value=0.0)
bedrooms = st.number_input("Number of Bedrooms", min_value=0)

# Predict Button
if st.button("Predict Price"):
    
    # Model expects 2 features
    features = np.array([[area,bedrooms,0]])  # Default garden=0 and price=0 for prediction
    
    prediction = model.predict(features)
    
    st.success(f" Predicted Price: ₹ {prediction[0]:,.2f}")