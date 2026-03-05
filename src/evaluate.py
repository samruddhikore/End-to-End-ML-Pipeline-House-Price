# src/evaluate.py

import pickle
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from data_cleaning import load_data, clean_data
from feature_engineering import select_features


def evaluate_model():

    df = load_data("data/housing.csv")
    df = clean_data(df)

    X, y = select_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    with open("models/model.pkl", "rb") as f:
        model = pickle.load(f)

    predictions = model.predict(X_test)

    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print("Model Evaluation Results")
    print("MSE:", mse)
    print("R2 Score:", r2)


if __name__ == "__main__":
    evaluate_model()