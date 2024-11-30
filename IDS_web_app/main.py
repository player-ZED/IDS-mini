from flask import Flask, request, render_template
import pandas as pd
import joblib
import numpy as np

app = Flask(__name__)

# Load the model and scaler
model = joblib.load('best_rf_model.pkl')
scaler = joblib.load('scaler.pkl')

# Define the route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define the route for predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']

    # Read the uploaded CSV file
    new_data = pd.read_csv(file)

    # Preprocess the data
    new_data.columns = new_data.columns.str.strip()
    new_data['Label'] = new_data['Label'].map({'BENIGN': 0, 'DDoS': 1})

    # Drop unnecessary columns (same as in your training)
    new_data = new_data.drop(columns=['Flow Bytes/s', 'Flow Packets/s','Bwd URG Flags', 'Bwd PSH Flags','Fwd URG Flags', 'CWE Flag Count','Bwd Avg Bulk Rate', 'Bwd Avg Bytes/Bulk','Fwd Avg Bytes/Bulk', 'Fwd Avg Bulk Rate','Bwd Avg Packets/Bulk', 'Fwd Avg Packets/Bulk'],errors='ignore')

    # Separate features
    X_new = new_data.drop(columns=['Label'])

    # Normalize the new data
    X_new_normalized = scaler.transform(X_new)

    # Make predictions
    predictions = model.predict(X_new_normalized)

    # Convert predictions to a DataFrame for easier display
    results = pd.DataFrame(predictions, columns=['Prediction'])

    # Convert predictions to human-readable labels
    results['Prediction'] = results['Prediction'].map({0: 'BENIGN', 1: 'DDoS'})

    return results.to_html()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
