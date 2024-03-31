import argparse
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score
import numpy as np
import pickle

# Parse the command-line arguments
parser = argparse.ArgumentParser(description='Analyze Temperature Data')
parser.add_argument('-u', '--uri', required=True, help="mongodb uri with username/password")
args = parser.parse_args()

# MongoDB setup
mongo_uri = args.uri
mongo_db = "mdmtemp"
mongo_collection = "mdmtemp"

client = MongoClient(mongo_uri)
db = client[mongo_db]
collection = db[mongo_collection]

# Fetch all documents
documents = list(collection.find(projection={"_id": 0}))

# Load data into a DataFrame
df = pd.DataFrame(documents)
df['year'] = pd.to_numeric(df['year'])
df['no_smoothing'] = pd.to_numeric(df['no_smoothing'])
df['lowess_5'] = pd.to_numeric(df['lowess_5'])

# Define input and output
X = df[['year']]
y = df['no_smoothing']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Linear Regression
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
linear_preds_test = linear_model.predict(X_test)
print(f"Linear Regression R^2 Score: {r2_score(y_test, linear_preds_test):.2f}")

# Polynomial Regression
degree = 3
poly_model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
poly_model.fit(X_train, y_train)
poly_preds_test = poly_model.predict(X_test)
print(f"Polynomial Regression (Degree {degree}) R^2 Score: {r2_score(y_test, poly_preds_test):.2f}")

# Random Forest
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_preds_test = rf_model.predict(X_test)
print(f"Random Forest R^2 Score: {r2_score(y_test, rf_preds_test):.2f}")

# Predictions for 2030, 2040, 2050
future_years = np.array([[2030], [2040], [2050]])
linear_preds = linear_model.predict(future_years)
poly_preds = poly_model.predict(future_years)
rf_preds = rf_model.predict(future_years)

# Printing predictions
print("\nPredictions for Temperature Anomaly (°C):")
for year, linear, poly, rf in zip(future_years.flatten(), linear_preds, poly_preds, rf_preds):
    print(f"\nYear: {year}")
    print(f"  Linear Regression: {linear:.2f}°C")
    print(f"  Polynomial Regression (Degree {degree}): {poly:.2f}°C")
    print(f"  Random Forest: {rf:.2f}°C")

# Save the models
with open('linear_regression_model.pkl', 'wb') as f:
    pickle.dump(linear_model, f)

with open('polynomial_regression_model.pkl', 'wb') as f:
    pickle.dump(poly_model, f)

with open('random_forest_model.pkl', 'wb') as f:
    pickle.dump(rf_model, f)
