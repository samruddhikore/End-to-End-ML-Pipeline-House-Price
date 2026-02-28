# House Price ML Prediction Project

A machine learning project to predict house prices based on various features using linear regression.

## Project Structure

```
house-price-ml/
├── data/
│   └── housing.csv (Training data)
├── src/
│   ├── train.py (Model training script)
│   └── predict.py (Prediction script)
├── app.py (Streamlit web application)
├── model.pkl (Trained model)
├── requirements.txt (Project dependencies)
└── README.md (This file)
```

## Installation

1. Clone or download this project
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Training the Model

Run the training script:
```bash
python src/train.py
```

This will train the linear regression model on the housing data and save it as `model.pkl`.

### Making Predictions

To make predictions, you can either:

1. Run the prediction script directly:
   ```bash
   python src/predict.py
   ```

2. Use the Streamlit web application:
   ```bash
   streamlit run app.py
   ```

## Dataset

The dataset includes the following features:
- **longitude**: Geographic longitude coordinate
- **latitude**: Geographic latitude coordinate
- **housing_median_age**: Median age of houses in the area
- **total_rooms**: Total number of rooms
- **total_bedrooms**: Total number of bedrooms
- **population**: Population in the area
- **households**: Number of households
- **median_income**: Median income
- **median_house_value**: Target variable (median house value)

## Model

The project uses a Linear Regression model from scikit-learn for predictions.

## Requirements

- Python 3.7+
- pandas
- numpy
- scikit-learn
- streamlit

## Author

Created for house price prediction machine learning project.

## License

MIT License
