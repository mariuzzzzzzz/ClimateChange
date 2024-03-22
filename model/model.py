# new terminal
# cd model
# python model.py -u 'MONGO_DB_CONNECTION_STRING'

import argparse
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline
import numpy as np

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

# Basic Analysis
# plt.figure(figsize=(10, 6))
# plt.plot(df['year'], df['no_smoothing'], label='No Smoothing')
# plt.plot(df['year'], df['lowess_5'], label='Lowess(5)')
# plt.xlabel('Year')
# plt.ylabel('Temperature Anomaly (°C)')
# plt.title('Global Mean Temperature Anomalies')
# plt.legend()
# plt.show()

# Define input and output
X = df[['year']]
y = df['no_smoothing']

# Linear Regression
linear_model = LinearRegression()
linear_model.fit(X, y)

# Polynomial Regression
degree = 3
poly_model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
poly_model.fit(X, y)

# Random Forest
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X, y)

# Predictions for 2030, 2040, 2050
future_years = np.array([[2030], [2040], [2050]])

# Linear Model Predictions
linear_preds = linear_model.predict(future_years)

# Polynomial Model Predictions
poly_preds = poly_model.predict(future_years)

# Random Forest Predictions
rf_preds = rf_model.predict(future_years)

# Printing predictions
print("Predictions for Temperature Anomaly (°C):")
for year, linear, poly, rf in zip(future_years.flatten(), linear_preds, poly_preds, rf_preds):
    print(f"\nYear: {year}")
    print(f"  Linear Regression: {linear:.2f}°C")
    print(f"  Polynomial Regression (Degree {degree}): {poly:.2f}°C")
    print(f"  Random Forest: {rf:.2f}°C")

#import
import pickle

# Save the Linear Regression model
with open('linear_regression_model.pkl', 'wb') as f:
    pickle.dump(linear_model, f)

# Save the Polynomial Regression model
with open('polynomial_regression_model.pkl', 'wb') as f:
    pickle.dump(poly_model, f)

# Save the Random Forest model
with open('random_forest_model.pkl', 'wb') as f:
    pickle.dump(rf_model, f)