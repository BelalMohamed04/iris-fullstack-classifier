import os

import requests
import streamlit as st


API_URL = os.getenv("API_URL", "http://localhost:8000").rstrip("/")

st.set_page_config(page_title="Iris Classifier")
st.title("Iris Classifier")
st.write("Enter the flower's measurements in centimetres to predict its species.")

with st.form("measurements"):
    sepal_length = st.number_input(
        "Sepal length (cm)", min_value=0.01, value=5.1, step=0.1, format="%.2f"
    )
    sepal_width = st.number_input(
        "Sepal width (cm)", min_value=0.01, value=3.5, step=0.1, format="%.2f"
    )
    petal_length = st.number_input(
        "Petal length (cm)", min_value=0.01, value=1.4, step=0.1, format="%.2f"
    )
    petal_width = st.number_input(
        "Petal width (cm)", min_value=0.01, value=0.2, step=0.1, format="%.2f"
    )
    submitted = st.form_submit_button("Predict species", type="primary")

if submitted:
    measurements = [sepal_length, sepal_width, petal_length, petal_width]
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json={"feature_array": measurements},
            timeout=10,
        )
        response.raise_for_status()
        species = response.json()["prediction"]["class_name"]
        if not isinstance(species, str) or not species:
            raise TypeError("Expected a species name")
    except requests.RequestException:
        st.error("The prediction service could not complete the request. Try again.")
    except (KeyError, TypeError):
        st.error("The prediction service returned an unexpected result.")
    else:
        st.success(f"Predicted species: {species.capitalize()}")
