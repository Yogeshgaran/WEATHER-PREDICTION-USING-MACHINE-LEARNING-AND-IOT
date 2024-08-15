import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import serial
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load user emails into a Pandas DataFrame
users_data = pd.read_csv('users.csv')  # Make sure you have a column 'email' in this CSV

# Load your weather data into a Pandas DataFrame
data = pd.read_csv('weather.csv')
le = LabelEncoder()
data['Summary_encoded'] = le.fit_transform(data['Summary'])
independent_vars = ['Humidity', 'Temperature']
dependent_var = 'Summary_encoded'
X = data[independent_vars]
y = data[dependent_var].ravel()
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Email sender credentials
sender_email = "yogigaran@gmail.com"
sender_password = "Y2EORvx8zg1BqNc5"

# Set up the SMTP server
server = smtplib.SMTP('smtp-relay.brevo.com', 587)
server.starttls()
server.login(sender_email, sender_password)

def send_email(receiver_email, weather_prediction,humidity,temperature):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Your Daily Weather Prediction"
    body = f"The predicted weather summary for today is: {weather_prediction}\n Humidity:{humidity}\nTemperature:{temperature}"
    msg.attach(MIMEText(body, 'plain'))
    server.send_message(msg)
    del msg

# Set up the serial connection
ser = serial.Serial('COM8', 9600, timeout=1)
time.sleep(2)
try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            data = line.split(",")
            if len(data) == 2:
                humidity = float(data[0])
                temperature = float(data[1])
                print(humidity)
                print(temperature)
                input_features = pd.DataFrame([[humidity, temperature]], columns=independent_vars)
                predicted_summary_encoded = model.predict(input_features)
                predicted_summary = le.inverse_transform(predicted_summary_encoded)[0]
                print(f"Predicted Weather Summary: {predicted_summary}")
                
                # Send the prediction to all users in the users_data DataFrame
                for index, user in users_data.iterrows():
                    send_email(user['email'], predicted_summary,humidity,temperature)
                break  # Remove this break if you want it to run continuously
        time.sleep(1)
finally:
    ser.close()
    server.quit()
