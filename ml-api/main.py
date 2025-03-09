from fastapi import FastAPI, HTTPException
import tensorflow as tf
import numpy as np
import pandas as pd
from pydantic import BaseModel
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import joblib
import uvicorn
import shap
import seaborn as sns
import matplotlib.pyplot as plt
import io
import os
import base64

# Import Custom Attention Layer
from finance_model import AttentionLayer

# Ensure TensorFlow doesn't use GPU if unavailable
try:
    tf.config.set_visible_devices([], 'GPU')
except:
    pass

# Load model with custom AttentionLayer
try:
    model = tf.keras.models.load_model("savings_model.h5", custom_objects={"AttentionLayer": AttentionLayer})
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")

# Load pre-saved encoders & scalers
try:
    scaler = joblib.load("scaler.pkl")
    encoder = joblib.load("encoder.pkl")
except Exception as e:
    raise RuntimeError(f"Failed to load scaler or encoder: {e}")

# Load the dataset for SHAP and insights
input_dir = "./kaggle/input"
df = pd.read_csv(os.path.join(input_dir, "data.csv"))

# FastAPI app instance
app = FastAPI()

# Define request structure
class InputData(BaseModel):
    Income: float
    Age: int
    Dependents: int
    Disposable_Income: float
    Desired_Savings: float
    Groceries: float
    Transport: float
    Eating_Out: float
    Entertainment: float
    Utilities: float
    Healthcare: float
    Education: float
    Miscellaneous: float
    Occupation: str
    City_Tier: str

# Helper function to preprocess input data
def preprocess_input(data, encoder, scaler):
    df_input = pd.DataFrame([data.dict()])
    encoded_cat = encoder.transform(df_input[['Occupation', 'City_Tier']])
    encoded_cat_df = pd.DataFrame(encoded_cat, columns=encoder.get_feature_names_out())
    df_numerical = df_input.drop(columns=['Occupation', 'City_Tier'])
    scaled_numerical = scaler.transform(df_numerical)
    df_scaled_numerical = pd.DataFrame(scaled_numerical, columns=df_numerical.columns)
    X_input = pd.concat([df_scaled_numerical, encoded_cat_df], axis=1)
    return X_input

# Endpoint 1: Predict potential savings
@app.post("/predict/")
def predict(data: InputData):
    try:
        X_input = preprocess_input(data, encoder, scaler)
        prediction = model.predict(X_input)
        target_columns = [
            'Potential_Savings_Groceries', 'Potential_Savings_Transport',
            'Potential_Savings_Eating_Out', 'Potential_Savings_Entertainment',
            'Potential_Savings_Utilities', 'Potential_Savings_Healthcare',
            'Potential_Savings_Education', 'Potential_Savings_Miscellaneous'
        ]
        prediction_dict = {col: float(prediction[0][i]) for i, col in enumerate(target_columns)}
        return {"Potential_Savings": prediction_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

# Endpoint 3: Perform scenario analysis
@app.post("/scenario-analysis/")
def scenario_analysis(data: InputData, income_increase: float = 0.1):
    try:
        X_input = preprocess_input(data, encoder, scaler)
        X_input['Income'] = X_input['Income'] * (1 + income_increase)
        prediction = model.predict(X_input)
        target_columns = [
            'Potential_Savings_Groceries', 'Potential_Savings_Transport',
            'Potential_Savings_Eating_Out', 'Potential_Savings_Entertainment',
            'Potential_Savings_Utilities', 'Potential_Savings_Healthcare',
            'Potential_Savings_Education', 'Potential_Savings_Miscellaneous'
        ]
        prediction_dict = {col: float(prediction[0][i]) for i, col in enumerate(target_columns)}
        return {"Scenario_Analysis": prediction_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scenario analysis failed: {e}")

# Endpoint 4: Get user segmentation
@app.post("/user-segmentation/")
def user_segmentation(data: InputData):
    try:
        X_input = preprocess_input(data, encoder, scaler)
        prediction = model.predict(X_input)
        total_savings = np.sum(prediction)
        if total_savings < 1000:
            segment = "Low Saver"
        elif total_savings < 5000:
            segment = "Medium Saver"
        else:
            segment = "High Saver"
        return {"User_Segment": segment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"User segmentation failed: {e}")

# Run FastAPI app if executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
