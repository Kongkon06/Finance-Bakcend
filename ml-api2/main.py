from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Load the trained model and feature list
model_path = "satej/models/linear_regression.pkl"
feature_columns_path = "satej/models/feature_columns.pkl"
lr_model = joblib.load(model_path)
feature_columns = joblib.load(feature_columns_path)

def preprocess_input(input_data):
    """
    Preprocess the input JSON data to match the model's requirements.
    """
    # Convert JSON to DataFrame
    df = pd.DataFrame([input_data])

    # Add missing columns with default values
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0  # Default value for missing features

    # Ensure correct data types
    numeric_cols = df.select_dtypes(include=np.number).columns
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    # Select and order features
    X = df[feature_columns]

    # Handle missing values
    X = X.fillna(X.mean())  # Simple imputation

    return X

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input JSON data
        input_data = request.json

        # Preprocess input
        processed_data = preprocess_input(input_data)

        # Predict 1-year returns
        predicted_1yr_return = lr_model.predict(processed_data)[0]

        # For 3-year and 5-year returns, use historical data (if available)
        # If not available, use a simple heuristic (e.g., scaling 1-year returns)
        predicted_3yr_return = predicted_1yr_return * 3  # Example scaling
        predicted_5yr_return = predicted_1yr_return * 5  # Example scaling

        # Return predictions
        return jsonify({
            "status": "success",
            "predictions": {
                "1_year_return": float(predicted_1yr_return),
                "3_year_return": float(predicted_3yr_return),
                "5_year_return": float(predicted_5yr_return),
            }
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
