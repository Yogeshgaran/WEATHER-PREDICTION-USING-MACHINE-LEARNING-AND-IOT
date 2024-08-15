import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import serial
import time

# Load your weather data into a Pandas DataFrame
data = pd.read_csv('weather.csv')  # Replace with the path to your dataset

# Encode the 'Summary' categorical data into numeric values
le = LabelEncoder()
data['Summary_encoded'] = le.fit_transform(data['Summary'])

# Select independent variables (features) and dependent variable (target)
independent_vars = ['Humidity', 'Temperature']
dependent_var = 'Summary_encoded'

# Separate the data into X (independent variables) and y (dependent variable)
X = data[independent_vars]
y = data[dependent_var].ravel()  # Flatten y to be one-dimensional

# Create and train a Random Forest Classifier model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Set up the serial connection (the port name will vary based on the computer)
ser = serial.Serial('COM8', 9600, timeout=1)  # Adjust 'COM8' to match your port
time.sleep(2)  # wait for the serial connection to initialize

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        data = line.split(",")
        
        if len(data) == 2:  # Check if the data has two elements (humidity and temperature)
            try:
                humidity = float(data[0])
                temperature = float(data[1])
                
                # Prepare the DataFrame for prediction with the correct column names
                input_features = pd.DataFrame([[humidity, temperature]], columns=independent_vars)
                
                # Make prediction using the model
                predicted_summary_encoded = model.predict(input_features)
                predicted_summary = le.inverse_transform(predicted_summary_encoded)
                
                print(f"Predicted Weather Summary: {predicted_summary[0]}")
            except ValueError:
                print("Invalid data received")
        time.sleep(1)  # Wait a bit before reading again to avoid flooding with data
