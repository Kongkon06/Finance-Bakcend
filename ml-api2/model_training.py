import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error, r2_score
import numpy as np


def train_linear_regression(X_train, y_train):
   model = LinearRegression()
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
   predictions = model.predict(X_test)
    mape = mean_absolute_percentage_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)  # Manually calculate RMSE
    r2 = r2_score(y_test, predictions)
    return {"MAPE": mape, "RMSE": rmse, "R2": r2}


if __name__ == "__main__":
    input_file = "satej/engineered_mutual_fund_data.csv"

    print("Loading engineered data...")
    data = pd.read_csv(input_file)

    print("Preparing data for model training...")
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

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training Linear Regression model...")
    lr_model = train_linear_regression(X_train, y_train)

    print("Evaluating Linear Regression model...")
    metrics = evaluate_model(lr_model, X_test, y_test)
    print(f"Linear Regression Metrics: {metrics}")
