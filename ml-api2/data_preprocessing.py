import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler

def load_data(file_path):
       if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_csv(file_path)


def clean_data(df):
       missing_summary = df.isnull().sum()
    print(f"Missing Values Summary:\n{missing_summary}")

    # Drop rows with missing 'scheme_name'
    if 'scheme_name' in df.columns:
        df = df.dropna(subset=['scheme_name'])
    else:
        raise ValueError("'scheme_name' column is missing in the raw dataset.")

    # Fill missing numerical values with forward-fill and backward-fill
    numerical_columns = ['min_sip', 'min_lumpsum', 'expense_ratio', 'fund_size_cr', 'fund_age_yr',
                         'sortino', 'alpha', 'sd', 'beta', 'sharpe', 'returns_1yr', 'returns_3yr', 'returns_5yr']
    for col in numerical_columns:
        df[col] = df[col].ffill().bfill()

    # Handle non-numeric values in numerical columns (e.g., '-')
    for col in numerical_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert non-numeric values to NaN
        df[col] = df[col].ffill().bfill()  # Fill any new NaNs created by the conversion

    return df


def preprocess_data(df):
   categorical_columns = ['risk_level', 'rating']
    df = pd.get_dummies(df, columns=categorical_columns, drop_first=True)

    # Scale numerical features
    numerical_columns = ['min_sip', 'min_lumpsum', 'expense_ratio', 'fund_size_cr', 'fund_age_yr',
                         'sortino', 'alpha', 'sd', 'beta', 'sharpe', 'returns_1yr', 'returns_3yr', 'returns_5yr']
    scaler = StandardScaler()
    df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

    return df


def save_cleaned_data(df, output_path):
   required_columns = ['scheme_name', 'fund_manager', 'amc_name', 'category', 'sub_category']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"'{col}' column is missing in the DataFrame.")

    # Reset the index to include the 'date' column in the CSV
    df.reset_index(inplace=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to: {output_path}")


if __name__ == "__main__":
    # Example usage
    input_file = "satej/mutual_fund_data.csv"
    output_file = "satej/cleaned_mutual_fund_data.csv"

    print("Loading data...")
    data = load_data(input_file)

    print("Cleaning data...")
    cleaned_data = clean_data(data)

    print("Preprocessing data...")
    preprocessed_data = preprocess_data(cleaned_data)

    print("Saving cleaned data...")
    save_cleaned_data(preprocessed_data, output_file)
