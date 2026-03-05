# train.py

import pandas as pd
import os
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


def load_data(path):
    try:
        df = pd.read_csv(path)
        print("Dataset loaded successfully!")
        return df
    except Exception as e:
        print("Error loading dataset:", e)
        return None


def clean_data(df):
    df = df.dropna()
    df = df.drop_duplicates()
    print("Data cleaned successfully!")
    return df


def select_features(df):
    # IMPORTANT: Explicitly define feature columns
    feature_columns = ['sqft', 'bedrooms', 'garden']   # change if needed
    target_column = 'price'

    X = df[feature_columns]
    y = df[target_column]

    print("Feature selection completed!")
    print("Using features:", feature_columns)

    return X, y


def train_and_evaluate():

    print("Loading dataset...")
    df = load_data("data/housing.csv")

    if df is None:
        return

    df = clean_data(df)

    X, y = select_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training model...")
    model = LinearRegression()
    model.fit(X_train, y_train)

    print("Model trained successfully!")
    print("Model expects", model.n_features_in_, "features")

    # Save model
    os.makedirs("models", exist_ok=True)

    with open("models/model.pkl", "wb") as f:
        pickle.dump(model, f)

    print("✅ Model saved successfully!")

    # Evaluate model
    predictions = model.predict(X_test)

    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print("\nModel Evaluation:")
    print("MSE:", mse)
    print("R2 Score:", r2)


if __name__ == "__main__":
    train_and_evaluate()