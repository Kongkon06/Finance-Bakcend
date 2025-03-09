import os
import pandas as pd
from data_preprocessing import load_data, clean_data, preprocess_data
from feature_engineering import (
    calculate_interaction_features,
    calculate_risk_adjusted_returns,
    calculate_performance_metrics,
    encode_categorical_features,
)
from model_training import train_linear_regression


def update_data(source_file, cleaned_file):
    """
    Automate the process of updating and cleaning new data.

    Args:
        source_file (str): Path to the raw data file.
        cleaned_file (str): Path to save the cleaned data.
    """
    print("Updating data...")
    raw_data = load_data(source_file)
    cleaned_data = clean_data(raw_data)
    preprocessed_data = preprocess_data(cleaned_data)
    preprocessed_data.to_csv(cleaned_file, index=False)
    print(f"Data updated and saved to {cleaned_file}")


def engineer_features(cleaned_file, engineered_file):
    """
    Automate the process of feature engineering.

    Args:
        cleaned_file (str): Path to the cleaned data file.
        engineered_file (str): Path to save the feature-engineered data.
    """
    print("Engineering features...")
    data = pd.read_csv(cleaned_file)

    # Calculate interaction features
    data = calculate_interaction_features(data)

    # Calculate risk-adjusted returns
    data = calculate_risk_adjusted_returns(data)

    # Calculate performance metrics
    data = calculate_performance_metrics(data)

    # Encode categorical features
    data = encode_categorical_features(data)

    # Save engineered data
    data.to_csv(engineered_file, index=False)
    print(f"Features engineered and saved to {engineered_file}")


def retrain_models(engineered_file, model_save_path):
    """
    Automate the process of retraining models.

    Args:
        engineered_file (str): Path to the feature-engineered data.
        model_save_path (str): Path to save trained models.
    """
    print("Retraining models...")
    data = pd.read_csv(engineered_file)

    # Define features and target variable
    target_column = "returns_1yr"  # Replace with your target variable
    features = [
        col
        for col in data.columns
        if col
        not in [
            target_column,
            "scheme_name",
            "fund_manager",
            "amc_name",
            "category",
            "sub_category",
        ]
    ]
    X = data[features].dropna()
    y = data[target_column][X.index]

    # Retrain Linear Regression
    print("Training Linear Regression model...")
    lr_model = train_linear_regression(X, y)

    # Save models
    os.makedirs(model_save_path, exist_ok=True)
    pd.to_pickle(lr_model, os.path.join(model_save_path, "linear_regression.pkl"))

    print(f"Models saved to {model_save_path}")


if __name__ == "__main__":
    source_file = "satej/mutual_fund_data.csv"
    cleaned_file = "satej/cleaned_mutual_fund_data.csv"
    engineered_file = "satej/engineered_mutual_fund_data.csv"
    model_save_path = "satej/models/"

    print("Starting automation pipeline...")
    update_data(source_file, cleaned_file)
    engineer_features(cleaned_file, engineered_file)
    retrain_models(engineered_file, model_save_path)
    print("Pipeline execution completed.")
