# src/feature_engineering.py

def select_features(df):
    # Example: Assume last column is target
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    print("Feature selection completed!")
    return X, y