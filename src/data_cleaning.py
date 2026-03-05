# src/data_cleaning.py

import pandas as pd

def load_data(path):
    try:
        df = pd.read_csv(path)
        print("Dataset loaded successfully!")
        return df
    except Exception as e:
        print("Error loading dataset:", e)
        return None


def clean_data(df):
    # Drop missing values
    df = df.dropna()

    # Remove duplicate rows
    df = df.drop_duplicates()

    print("Data cleaned successfully!")
    return df