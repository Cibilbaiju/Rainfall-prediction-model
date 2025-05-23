from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Load trained ML model
with open('rainfall_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load model accuracy from text file and convert to float
with open('model_accuracy.txt', 'r') as acc_file:
    model_accuracy = float(acc_file.read().strip())

# Home page — input form
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', accuracy=model_accuracy)

# Report page — prediction results + chart
@app.route('/report', methods=['POST'])
def report():
    try:
        # Collect and validate input values
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        pressure = float(request.form['pressure'])
        wind_speed = float(request.form['wind_speed'])

        # Prepare features for prediction
        input_features = np.array([[temperature, humidity, pressure, wind_speed]])
        prediction = model.predict(input_features)[0]
        prediction = max(0, round(prediction, 2))

        # Render report page with prediction and model accuracy
        return render_template(
            'report.html',
            temperature=temperature,
            humidity=humidity,
            pressure=pressure,
            wind_speed=wind_speed,
            prediction=prediction,
            accuracy=model_accuracy
        )

    except ValueError:
        return "Invalid input. Please enter valid numeric values."

# Visualization page — dotted rainfall graph
@app.route('/visualization')
def visualization():
    try:
        # Load rainfall dataset
        data = pd.read_csv('data/navi_mumbai_rainfall.csv')

        # Check for required columns
        if 'Temperature (C)' not in data.columns or 'Rainfall (mm)' not in data.columns:
            return "Error: Required columns missing in the dataset."

        # Group by Month if available, else generate fallback labels
        if 'Month' in data.columns:
            avg_rainfall = data.groupby('Month')['Rainfall (mm)'].mean().round(2).to_dict()
            labels = list(avg_rainfall.keys())
            values = list(avg_rainfall.values())
        else:
            labels = list(range(1, len(data) + 1))
            values = data['Rainfall (mm)'].round(2).tolist()

        return render_template('visualization.html', labels=labels, values=values)

    except Exception as e:
        return f"Error loading visualization data: {e}"

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
