# ==========================================
# IMPORT LIBRARIES
# ==========================================

import streamlit as st
import pandas as pd
import pickle

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Social Media Addiction Detector",
    page_icon="📱",
    layout="centered"
)

# ==========================================
# LOAD TRAINED MODEL
# ==========================================

with open("../models/addiction_model.pkl", "rb") as file:
    model = pickle.load(file)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title(" Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "🏠 Home",
        "📊 Analytics",
        "ℹ️ About"
    ]
)
st.sidebar.markdown("---")

st.sidebar.header("About the Project")

st.sidebar.write("""
This application predicts a student's **Social Media Addiction Level**
using a Machine Learning model trained on behavioural and lifestyle data.
""")

st.sidebar.markdown("---")

st.sidebar.header("Technology Stack")

st.sidebar.markdown("""
-  Python
-  Pandas
-  Scikit-learn
-  Streamlit
-  Matplotlib & Seaborn
""")

st.sidebar.markdown("---")

st.sidebar.header("Machine Learning Model")

st.sidebar.success("Random Forest Classifier")

st.sidebar.markdown("---")

st.sidebar.info(
    "Complete the form on the right and click **Predict Addiction Level**."
)

# ==========================================
# APPLICATION HEADER
# ==========================================
if page == "🏠 Home":
    st.title(" Social Media Addiction Detection System")

    st.markdown("""
    This AI-powered system predicts social media addiction levels
    based on lifestyle, screen-time, and behavioral patterns.
    """)

    st.write("Enter details to predict addiction level.")

    # ==========================================
    # USER INPUTS
    # ==========================================
    st.subheader(" Personal Information")
    age = st.slider("Age", 18, 30, 20)

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    academic_level = st.selectbox(
        "Academic Level",
        ["High School", "Undergraduate", "Graduate"]
    )
    country = st.selectbox(
        "Country",
        ["India", "USA", "UK", "Canada", "Australia"]
    )

    st.subheader(" Social Media Usage")
    avg_daily_usage = st.slider(
        "Average Daily Usage Hours",
        1.0,
        12.0,
        5.0
    )
    most_used_platform = st.selectbox(
        "Most Used Platform",
        ["Instagram", "TikTok", "YouTube", "Facebook", "Twitter", "Snapchat", "LinkedIn"]
    )
    conflicts_over_social_media = st.slider(
        "Conflicts Over Social Media",
        0,
        10,
        2
    )
    affects_academic_performance = st.selectbox(
        "Affects Academic Performance",
        ["Yes", "No"]
    )

    st.subheader(" Lifestyle & Well-being")
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

    relationship_status = st.selectbox(
        "Relationship Status",
        ["Single", "In Relationship", "Complicated"]
    )

    # ==========================================
    # DATA ENCODING
    # ==========================================
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

# ==========================================
# PREDICTION
# ==========================================
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
        probabilities = model.predict_proba(input_data)
        confidence = probabilities.max() * 100

        addiction_labels = {
            0: "Low Addiction",
            1: "Medium Addiction",
            2: "High Addiction"
        }

        result = addiction_labels[prediction[0]]

    # ==========================================
    # RECOMMENDATIONS
    # ==========================================
        st.markdown("---")
        st.subheader("🧠 Prediction Results")

        if result == "Low Addiction":
            st.success("🟢 LOW ADDICTION")
            risk = "Low"

        elif result == "Medium Addiction":
            st.warning("🟡 MEDIUM ADDICTION")
            risk = "Medium"

        else:
            st.error("🔴 HIGH ADDICTION")
            risk = "High"

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label="Model Confidence",
                value=f"{confidence:.2f}%"
            )

        with col2:
            st.metric(
                label="Risk Level",
                value=risk
            )
        st.markdown("---")
        st.subheader("📌 Personalized Recommendations")

        recommendations = []

        if avg_daily_usage >= 8:
            recommendations.append(
                "Reduce your daily social media usage gradually by setting screen-time limits."
            )

        if sleep_hours < 6:
            recommendations.append(
                "Increase your sleep duration to at least 7–8 hours each night."
            )

        if mental_health_score <= 4:
            recommendations.append(
                "Consider reducing late-night screen time and prioritizing activities that support your mental well-being."
            )

        if conflicts_over_social_media >= 4:
            recommendations.append(
                "Frequent conflicts related to social media may indicate unhealthy usage. Consider taking regular digital detox breaks."
            )

        if result == "High Addiction":
            recommendations.append(
                "Consider using app timers or digital well-being tools to monitor and reduce social media usage."
            )

        elif result == "Medium Addiction":
            recommendations.append(
                "Maintain healthy habits and monitor your screen time to prevent increased dependency."
            )

        else:
            recommendations.append(
                "Great job! Your current habits indicate a healthy balance between digital life and personal well-being."
            )
        for recommendation in recommendations:
            st.info(recommendation)
    # ==========================================
    # FOOTER
    # ==========================================

        st.markdown("---")

        st.caption(
            "Developed by Kush Sharma | AI/ML Internship Project | Streamlit + Scikit-learn"
        )
 # ==========================================
 # Analytic block
# ==========================================

elif page == "📊 Analytics":

    st.title("📊 Dataset Analytics")

    st.write(
        "Explore the dataset used to train the Social Media Addiction Detection model."
    )

    df = pd.read_csv("../data/Students Social Media Addiction.csv")
    def classify_addiction(score):
        if score <= 4:
            return "Low"
        elif score <= 7:
            return "Medium"
        else:
            return "High"

    df["Addiction_Level"] = df["Addicted_Score"].apply(classify_addiction)
    st.subheader("Dataset Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    with col3:
        st.metric("Missing Values", df.isnull().sum().sum())

    st.markdown("---")

    st.subheader("Dataset Preview")

    st.dataframe(df.head())

    st.markdown("---")
    st.subheader("📊 Addiction Level Distribution")

    addiction_counts = df["Addiction_Level"].value_counts()

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor("none")
    ax.set_facecolor("none")
    ax.set_title(
        "Distribution of Addiction Levels",
        color="white",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel("Addiction Level", color="white")
    ax.set_ylabel("Number of Students", color="white")

    ax.tick_params(colors="white")

    addiction_counts.plot(kind="bar", ax=ax, color=["#2ecc71", "#f1c40f", "#e74c3c"])

    ax.set_xlabel("Addiction Level")
    ax.set_ylabel("Number of Students")
    ax.set_title("Distribution of Addiction Levels")

    st.pyplot(fig)