import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import pickle
import os

print("Current working directory is:", os.getcwd())

# Load data
try:
    data = pd.read_csv('data/navi_mumbai_rainfall.csv')
    print("✅ Data loaded successfully.")
except FileNotFoundError:
    print("❌ Data file not found.")
    exit()

if data.isnull().values.any():
    print("❌ Data contains missing values.")
    exit()

try:
    X = data[['Temperature', 'Humidity', 'Pressure', 'WindSpeed']]
    y = data['Rainfall']
except KeyError as e:
    print(f"❌ Missing column: {e}")
    exit()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

model = RandomForestRegressor(n_estimators=200, random_state=0)
model.fit(X_train, y_train)

with open('rainfall_model.pkl', 'wb') as f:
    pickle.dump(model, f)

y_pred = model.predict(X_test)
accuracy = r2_score(y_test, y_pred)

print("✅ About to write accuracy to file...")

# Guarantee save location
accuracy_path = os.path.join(os.path.dirname(__file__), 'model_accuracy.txt')
with open(accuracy_path, 'w') as acc_file:
    acc_file.write(str(round(accuracy * 100, 2)))

print(f"✅ Accuracy saved successfully: {round(accuracy * 100, 2)}% at {accuracy_path}")
