import joblib
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def train_linear_regression(X_train, y_train):
    """
    Train a Linear Regression model.
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

if __name__ == "__main__":
    # Load engineered data
    input_file = "satej/engineered_mutual_fund_data.csv"
    data = pd.read_csv(input_file)

    # Define features and target variable
    target_column = "returns_1yr"
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

    # Prepare data
    X = data[features].dropna()
    y = data[target_column][X.index]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    print("Training Linear Regression model...")
    lr_model = train_linear_regression(X_train, y_train)

    # Save the model
    model_save_path = "satej/models/"
    os.makedirs(model_save_path, exist_ok=True)
    joblib.dump(lr_model, os.path.join(model_save_path, "linear_regression.pkl"))

    # Save the list of feature names
    joblib.dump(features, os.path.join(model_save_path, "feature_columns.pkl"))
    print(f"Model and feature list saved to {model_save_path}")
