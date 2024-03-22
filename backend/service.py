# python -m flask --debug --app service run

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import pickle
import numpy as np
from azure.storage.blob import BlobServiceClient

app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
CORS(app)

# Define the prefix for your model containers
MODEL_CONTAINER_PREFIX = "climatechange-model"


# Azure Storage Connection String
azure_storage_connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

# Initialize Azure Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)

# Find the latest container for models
def get_latest_model_container(container_prefix):
    highest_version = -1
    latest_container_name = ""
    
    containers = blob_service_client.list_containers(name_starts_with=container_prefix)
    for container in containers:
        version = int(container['name'].split('-')[-1])
        if version > highest_version:
            highest_version = version
            latest_container_name = container['name']
            
    if latest_container_name:
        print(f"Using latest model container: {latest_container_name}")
    else:
        print("No model containers found.")
        
    return latest_container_name

# Download and load a model from the specified container
def download_and_load_model(container_name, model_name):
    if container_name:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=model_name)
        blob_data = blob_client.download_blob().readall()
        model = pickle.loads(blob_data)
        print(f"Loaded model: {model_name}")
        return model
    else:
        print(f"Container not found for model: {model_name}")
        return None

# Load models dynamically from Azure Blob Storage
latest_container = get_latest_model_container(MODEL_CONTAINER_PREFIX)
model_names = ["linear_regression_model.pkl", "polynomial_regression_model.pkl", "random_forest_model.pkl"]
models = {model_name.split('.')[0]: download_and_load_model(latest_container, model_name) for model_name in model_names}

# Prediction API endpoint
@app.route("/api/predict", methods=["GET"])
def predict_temperature():
    year = request.args.get('year', default=2020, type=int)
    demo_input = np.array([[year]])
    
    predictions = {}
    for model_name, model in models.items():
        if model:
            predictions[model_name] = model.predict(demo_input)[0]
        else:
            predictions[model_name] = "Model not loaded"

    return jsonify(predictions)

# Serve Svelte static files and enable SPA routing
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(debug=True)
