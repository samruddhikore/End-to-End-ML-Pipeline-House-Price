# src/eda.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def perform_eda(path):

    print("Loading dataset...")
    df = pd.read_csv(path)

    print("\n🔹 First 5 Rows:")
    print(df.head())

    print("\n🔹 Dataset Info:")
    print(df.info())

    print("\n🔹 Missing Values:")
    print(df.isnull().sum())

    print("\n🔹 Statistical Summary:")
    print(df.describe())

    # -----------------------------
    # 1️⃣ Distribution Plots
    # -----------------------------
    print("\nGenerating Distribution Plots...")
    df.hist(figsize=(8, 6))
    plt.suptitle("Distribution of Features")
    plt.show()

    # -----------------------------
    # 2️⃣ Boxplots (Outlier Detection)
    # -----------------------------
    print("\nGenerating Boxplots...")
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df)
    plt.title("Boxplot of Features")
    plt.xticks(rotation=45)
    plt.show()

    # -----------------------------
    # 3️⃣ Correlation Heatmap
    # -----------------------------
    print("\nGenerating Correlation Heatmap...")
    plt.figure(figsize=(6, 4))
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
    plt.title("Feature Correlation Heatmap")
    plt.show()

    # -----------------------------
    # 4️⃣ Pairplot (Feature Relationships)
    # -----------------------------
    print("\nGenerating Pairplot...")
    sns.pairplot(df)
    plt.show()


if __name__ == "__main__":
    perform_eda("data/housing.csv")