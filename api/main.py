from fastapi import FastAPI 
from pydantic import BaseModel
import pickle 
import pandas as pd 

app = FastAPI(
    title="Social Media Addiction Prediction API",
    description="Backend API for Social Media Addiction Detection System",
    version="1.0"
)

# Load trained model
with open("models/addiction_model.pkl", "rb") as file:
    model = pickle.load(file)
class StudentData(BaseModel):
    Age: int
    Gender: int
    Academic_Level: int
    Country: int
    Avg_Daily_Usage_Hours: float
    Most_Used_Platform: int
    Affects_Academic_Performance: int
    Sleep_Hours_Per_Night: float
    Mental_Health_Score: int
    Relationship_Status: int
    Conflicts_Over_Social_Media: int

@app.get("/")
def home():
    return {
        "message": "Social Media Addiction Prediction API is Running!"
    }

@app.post("/predict")
def predict(data: StudentData):

    input_df = pd.DataFrame([data.model_dump()])

    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    confidence = float(max(probabilities) * 100)

    labels = {
        0: "Low Addiction",
        1: "Medium Addiction",
        2: "High Addiction"
    }

    return {
        "prediction": labels[prediction],
        "confidence": round(confidence, 2)
    }