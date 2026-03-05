"""
Data Analysis and Visualization Generation Script
Generates all necessary data, statistics, and visualizations for the HTML report
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import pickle
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Paths
DATA_PATH = Path("data/housing.csv")
REPORT_DIR = Path("report")
ASSETS_DIR = REPORT_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
DATA_DIR = ASSETS_DIR / "data"
MODELS_DIR = Path("models")

# Create directories if they don't exist
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

def load_data():
    """Load the housing dataset"""
    try:
        df = pd.read_csv(DATA_PATH)
        print("✓ Dataset loaded successfully!")
        return df
    except Exception as e:
        print(f"✗ Error loading dataset: {e}")
        return None

def dataset_statistics(df):
    """Calculate dataset statistics"""
    stats = {
        'rows': len(df),
        'columns': len(df.columns),
        'missing_values': df.isnull().sum().to_dict(),
        'duplicates': len(df[df.duplicated()]),
        'numerical_summary': df.describe().to_dict(),
        'data_types': df.dtypes.to_dict()
    }
    return stats

def correlation_analysis(df):
    """Calculate correlation matrix"""
    corr_matrix = df.corr()
    return corr_matrix

def generate_eda_visualizations(df):
    """Generate EDA visualizations"""
    
    # 1. Distribution plots
    print("Generating distribution plots...")
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    fig.suptitle('Feature Distributions', fontsize=16, fontweight='bold')
    
    columns = df.columns[:-1]  # Exclude target
    for idx, col in enumerate(columns):
        ax = axes[idx // 2, idx % 2]
        ax.hist(df[col], bins=30, color='steelblue', alpha=0.7, edgecolor='black')
        ax.set_xlabel(col, fontsize=10)
        ax.set_ylabel('Frequency', fontsize=10)
        ax.set_title(f'Distribution of {col}')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / 'eda_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Distribution plots saved")
    
    # 2. Box plots (outlier detection)
    print("Generating box plots...")
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Box Plots - Outlier Detection', fontsize=16, fontweight='bold')
    
    for idx, col in enumerate(columns):
        ax = axes[idx]
        ax.boxplot(df[col], vert=True)
        ax.set_ylabel(col, fontsize=10)
        ax.set_title(f'Box Plot of {col}')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / 'eda_boxplots.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Box plots saved")
    
    # 3. Correlation heatmap
    print("Generating correlation heatmap...")
    fig, ax = plt.subplots(figsize=(10, 8))
    corr_matrix = df.corr()
    sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0,
                square=True, ax=ax, cbar_kws={'label': 'Correlation'})
    ax.set_title('Feature Correlation Heatmap', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / 'eda_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Correlation heatmap saved")
    
    # 4. Pair plot (relationships)
    print("Generating pair plot...")
    pair_plot = sns.pairplot(df, diag_kind='hist', plot_kws={'alpha': 0.6}, diag_kws={'bins': 20})
    pair_plot.fig.suptitle('Pair Plot - Feature Relationships', fontsize=14, fontweight='bold', y=1.001)
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / 'eda_pairplot.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Pair plot saved")
    
    # 5. Target distribution
    print("Generating target variable plot...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Price Distribution', fontsize=16, fontweight='bold')
    
    axes[0].hist(df['price'], bins=30, color='#27ae60', alpha=0.7, edgecolor='black')
    axes[0].set_xlabel('Price', fontsize=10)
    axes[0].set_ylabel('Frequency', fontsize=10)
    axes[0].set_title('Histogram of Price')
    axes[0].grid(True, alpha=0.3)
    
    axes[1].scatter(range(len(df)), df['price'].sort_values(), alpha=0.5, color='#27ae60')
    axes[1].set_xlabel('Index (Sorted)', fontsize=10)
    axes[1].set_ylabel('Price', fontsize=10)
    axes[1].set_title('Price - Sorted View')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / 'eda_target.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Target distribution saved")
    
    # 6. Feature vs Target
    print("Generating feature vs target plots...")
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    fig.suptitle('Feature vs Target (Price)', fontsize=16, fontweight='bold')
    
    feature_cols = ['sqft', 'bedrooms', 'garden']
    for idx, col in enumerate(feature_cols):
        axes[idx].scatter(df[col], df['price'], alpha=0.5, color='#3498db')
        axes[idx].set_xlabel(col, fontsize=10)
        axes[idx].set_ylabel('Price', fontsize=10)
        axes[idx].set_title(f'{col} vs Price')
        
        # Add trend line
        z = np.polyfit(df[col], df['price'], 1)
        p = np.poly1d(z)
        axes[idx].plot(df[col].sort_values(), p(df[col].sort_values()), "r--", alpha=0.8, linewidth=2)
        axes[idx].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / 'eda_features_vs_target.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Feature vs target plots saved")

def train_and_evaluate_model(df):
    """Train the linear regression model and get evaluation metrics"""
    print("Training model...")
    
    # Prepare data
    feature_columns = ['sqft', 'bedrooms', 'garden']
    X = df[feature_columns]
    y = df['price']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Get predictions
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    # Calculate metrics
    train_mse = mean_squared_error(y_train, y_pred_train)
    test_mse = mean_squared_error(y_test, y_pred_test)
    train_rmse = np.sqrt(train_mse)
    test_rmse = np.sqrt(test_mse)
    train_mae = mean_absolute_error(y_train, y_pred_train)
    test_mae = mean_absolute_error(y_test, y_pred_test)
    train_r2 = r2_score(y_train, y_pred_train)
    test_r2 = r2_score(y_test, y_pred_test)
    
    # Save model
    with open(MODELS_DIR / "model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    print("✓ Model trained and saved")
    
    metrics = {
        'train_mse': float(train_mse),
        'test_mse': float(test_mse),
        'train_rmse': float(train_rmse),
        'test_rmse': float(test_rmse),
        'train_mae': float(train_mae),
        'test_mae': float(test_mae),
        'train_r2': float(train_r2),
        'test_r2': float(test_r2),
        'coefficients': {feat: float(coef) for feat, coef in zip(feature_columns, model.coef_)},
        'intercept': float(model.intercept_),
        'n_samples_train': len(X_train),
        'n_samples_test': len(X_test),
        'n_features': len(feature_columns)
    }
    
    return model, X_train, X_test, y_train, y_test, y_pred_train, y_pred_test, metrics

def generate_model_visualizations(model, X_test, y_test, y_pred_test):
    """Generate model evaluation visualizations"""
    
    print("Generating model evaluation plots...")
    
    # 1. Actual vs Predicted
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Model Predictions', fontsize=16, fontweight='bold')
    
    axes[0].scatter(y_test, y_pred_test, alpha=0.6, color='#3498db')
    axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    axes[0].set_xlabel('Actual Price', fontsize=10)
    axes[0].set_ylabel('Predicted Price', fontsize=10)
    axes[0].set_title('Actual vs Predicted Prices')
    axes[0].grid(True, alpha=0.3)
    
    # 2. Residuals plot
    residuals = y_test - y_pred_test
    axes[1].scatter(y_pred_test, residuals, alpha=0.6, color='#e74c3c')
    axes[1].axhline(y=0, color='r', linestyle='--', lw=2)
    axes[1].set_xlabel('Predicted Price', fontsize=10)
    axes[1].set_ylabel('Residuals', fontsize=10)
    axes[1].set_title('Residual Plot')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / 'model_predictions.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Model predictions plots saved")
    
    # 3. Feature Coefficients
    fig, ax = plt.subplots(figsize=(10, 6))
    feature_names = X_test.columns
    coefficients = model.coef_
    colors = ['#3498db' if c > 0 else '#e74c3c' for c in coefficients]
    
    bars = ax.barh(feature_names, coefficients, color=colors, edgecolor='black')
    ax.set_xlabel('Coefficient Value', fontsize=11)
    ax.set_title('Model Coefficients (Feature Importance)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    
    # Add value labels
    for i, (bar, coef) in enumerate(zip(bars, coefficients)):
        ax.text(coef, i, f' {coef:.2f}', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / 'model_coefficients.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Feature coefficients plot saved")
    
    # 4. Residuals distribution
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Residual Analysis', fontsize=16, fontweight='bold')
    
    axes[0].hist(residuals, bins=30, color='#9b59b6', alpha=0.7, edgecolor='black')
    axes[0].set_xlabel('Residuals', fontsize=10)
    axes[0].set_ylabel('Frequency', fontsize=10)
    axes[0].set_title('Distribution of Residuals')
    axes[0].grid(True, alpha=0.3)
    
    # Q-Q plot
    from scipy import stats
    stats.probplot(residuals, dist="norm", plot=axes[1])
    axes[1].set_title('Q-Q Plot')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / 'model_residuals.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Residuals analysis plots saved")

def generate_comparison_visualizations(X_train, X_test, y_train, y_test, y_pred_train, y_pred_test):
    """Generate train vs test comparison visualizations"""
    
    print("Generating comparison plots...")
    
    # Error distribution
    train_errors = y_train - y_pred_train
    test_errors = y_test - y_pred_test
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Training vs Testing Performance', fontsize=16, fontweight='bold')
    
    axes[0].hist([train_errors, test_errors], bins=20, label=['Train', 'Test'], 
                 color=['#27ae60', '#e74c3c'], alpha=0.7, edgecolor='black')
    axes[0].set_xlabel('Prediction Errors', fontsize=10)
    axes[0].set_ylabel('Frequency', fontsize=10)
    axes[0].set_title('Error Distribution')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Metrics comparison
    metrics_names = ['MSE', 'RMSE', 'MAE']
    train_metrics = [
        mean_squared_error(y_train, y_pred_train),
        np.sqrt(mean_squared_error(y_train, y_pred_train)),
        mean_absolute_error(y_train, y_pred_train)
    ]
    test_metrics = [
        mean_squared_error(y_test, y_pred_test),
        np.sqrt(mean_squared_error(y_test, y_pred_test)),
        mean_absolute_error(y_test, y_pred_test)
    ]
    
    x = np.arange(len(metrics_names))
    width = 0.35
    
    axes[1].bar(x - width/2, train_metrics, width, label='Train', color='#27ae60', edgecolor='black')
    axes[1].bar(x + width/2, test_metrics, width, label='Test', color='#e74c3c', edgecolor='black')
    axes[1].set_ylabel('Metric Value', fontsize=10)
    axes[1].set_title('Metrics Comparison')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(metrics_names)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / 'model_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Comparison plots saved")

def save_json_data(stats, corr_matrix, metrics):
    """Save data as JSON for easy access"""
    
    data = {
        'statistics': stats,
        'correlation': corr_matrix.to_dict(),
        'metrics': metrics
    }
    
    with open(DATA_DIR / 'analysis.json', 'w') as f:
        json.dump(data, f, indent=2, default=str)
    
    print("✓ Analysis data saved as JSON")

def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("DATA ANALYSIS & VISUALIZATION GENERATION")
    print("="*60 + "\n")
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    print(f"\nDataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nFirst few rows:")
    print(df.head())
    
    # Get statistics
    stats = dataset_statistics(df)
    print(f"\nDataset Statistics:")
    print(f"  - Total rows: {stats['rows']}")
    print(f"  - Total columns: {stats['columns']}")
    print(f"  - Missing values: {sum(stats['missing_values'].values())}")
    print(f"  - Duplicate rows: {stats['duplicates']}")
    
    # Generate EDA visualizations
    generate_eda_visualizations(df)
    
    # Correlation analysis
    corr_matrix = correlation_analysis(df)
    print(f"\nCorrelation with Price:")
    print(corr_matrix['price'].sort_values(ascending=False))
    
    # Train and evaluate model
    model, X_train, X_test, y_train, y_test, y_pred_train, y_pred_test, metrics = train_and_evaluate_model(df)
    
    print(f"\nModel Evaluation Metrics:")
    print(f"  - Train R² Score: {metrics['train_r2']:.4f}")
    print(f"  - Test R² Score: {metrics['test_r2']:.4f}")
    print(f"  - Train RMSE: ${metrics['train_rmse']:.2f}")
    print(f"  - Test RMSE: ${metrics['test_rmse']:.2f}")
    print(f"  - Train MAE: ${metrics['train_mae']:.2f}")
    print(f"  - Test MAE: ${metrics['test_mae']:.2f}")
    
    print(f"\nModel Coefficients:")
    for feat, coef in metrics['coefficients'].items():
        print(f"  - {feat}: {coef:.2f}")
    print(f"  - Intercept: {metrics['intercept']:.2f}")
    
    # Generate model visualizations
    generate_model_visualizations(model, X_test, y_test, y_pred_test)
    
    # Generate comparison visualizations
    generate_comparison_visualizations(X_train, X_test, y_train, y_test, y_pred_train, y_pred_test)
    
    # Save JSON data
    save_json_data(stats, corr_matrix, metrics)
    
    print("\n" + "="*60)
    print("✓ ALL VISUALIZATIONS AND ANALYSIS GENERATED SUCCESSFULLY!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
