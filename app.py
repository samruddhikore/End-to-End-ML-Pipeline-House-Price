import streamlit as st
import pickle
import numpy as np

with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("House Price Prediction App")

st.write("Enter house details:")

area = st.number_input("Area")
bedrooms = st.number_input("Bedrooms")

if st.button("Predict"):
    features = np.array([[area, bedrooms]])
    prediction = model.predict(features)
    st.success(f"Predicted Price: {prediction[0]}")