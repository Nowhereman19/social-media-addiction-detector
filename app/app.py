import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title="Social Media Addiction Detector",
    page_icon="📱",
    layout="centered"
)

# Load model
with open("../models/addiction_model.pkl", "rb") as file:
    model = pickle.load(file)

# App title
st.title("📱 Social Media Addiction Detection System")

st.markdown("""
This AI-powered system predicts social media addiction levels
based on lifestyle, screen-time, and behavioral patterns.
""")

st.write("Enter details to predict addiction level.")

# Inputs
age = st.slider("Age", 18, 30, 20)

avg_daily_usage = st.slider(
    "Average Daily Usage Hours",
    1.0,
    12.0,
    5.0
)

sleep_hours = st.slider(
    "Sleep Hours Per Night",
    1.0,
    12.0,
    7.0
)

mental_health_score = st.slider(
    "Mental Health Score",
    1,
    10,
    5
)

conflicts_over_social_media = st.slider(
    "Conflicts Over Social Media",
    0,
    10,
    2
)

gender = st.selectbox(
    "Gender",
    ["Male", "Female"]
)

academic_level = st.selectbox(
    "Academic Level",
    ["High School", "Undergraduate", "Graduate"]
)

most_used_platform = st.selectbox(
    "Most Used Platform",
    ["Instagram", "TikTok", "YouTube", "Facebook", "Twitter", "Snapchat", "LinkedIn"]
)

affects_academic_performance = st.selectbox(
    "Affects Academic Performance",
    ["Yes", "No"]
)

relationship_status = st.selectbox(
    "Relationship Status",
    ["Single", "In Relationship", "Complicated"]
)

country = st.selectbox(
    "Country",
    ["India", "USA", "UK", "Canada", "Australia"]
)

# Manual encoding
gender_map = {"Female": 0, "Male": 1}

academic_map = {
    "High School": 0,
    "Undergraduate": 1,
    "Graduate": 2
}

platform_map = {
    "Instagram": 0,
    "TikTok": 1,
    "YouTube": 2,
    "Facebook": 3,
    "Twitter": 4,
    "Snapchat": 5,
    "LinkedIn": 6
}

performance_map = {
    "No": 0,
    "Yes": 1
}

relationship_map = {
    "Single": 0,
    "In Relationship": 1,
    "Complicated": 2
}

country_map = {
    "India": 0,
    "USA": 1,
    "UK": 2,
    "Canada": 3,
    "Australia": 4
}

# Predict button
if st.button("Predict Addiction Level"):

    input_data = pd.DataFrame({
        "Age": [age],
        "Gender": [gender_map[gender]],
        "Academic_Level": [academic_map[academic_level]],
        "Country": [country_map[country]],
        "Avg_Daily_Usage_Hours": [avg_daily_usage],
        "Most_Used_Platform": [platform_map[most_used_platform]],
        "Affects_Academic_Performance": [performance_map[affects_academic_performance]],
        "Sleep_Hours_Per_Night": [sleep_hours],
        "Mental_Health_Score": [mental_health_score],
        "Relationship_Status": [relationship_map[relationship_status]],
        "Conflicts_Over_Social_Media": [conflicts_over_social_media]
    })

    prediction = model.predict(input_data)

    addiction_labels = {
        0: "Low Addiction",
        1: "Medium Addiction",
        2: "High Addiction"
    }

    result = addiction_labels[prediction[0]]

    if result == "Low Addiction":
        st.success(f"Predicted Addiction Level: {result}")

    elif result == "Medium Addiction":
        st.warning(f"Predicted Addiction Level: {result}")

    else:
        st.error(f"Predicted Addiction Level: {result}")
