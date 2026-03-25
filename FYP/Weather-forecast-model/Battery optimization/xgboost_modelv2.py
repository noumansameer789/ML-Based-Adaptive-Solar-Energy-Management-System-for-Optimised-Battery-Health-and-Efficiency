import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

# Load dataset (replace with your actual filename)
df = pd.read_csv("D:/Uni/FYP/Weather-forecast-model/Battery optimization/weather_data1.csv", encoding='latin1')

# Print initial dataset shape
print(f"Initial Data Shape: {df.shape}")

# Strip spaces and ensure proper column names
df.rename(columns=lambda x: x.strip(), inplace=True)

# Rename columns explicitly for clarity
df.rename(columns={'YEAR': 'year', 'MO': 'month', 'DY': 'day', 'HR': 'hour'}, inplace=True)

# Convert to datetime format
df['Datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']], errors='coerce')

# Sort data by time to ensure proper lag features
df = df.sort_values(by='Datetime')

# Create Lag Features (Previous Day's Data)
df['Prev_Temp'] = df['Temp at 2meter'].shift(1)  
df['Prev_Humidity'] = df['Humidity'].shift(1)  
df['Prev_WindSpeed'] = df['Wind speed'].shift(1)  
df['Prev_Irradiance'] = df['Irradiance wh/m^2'].shift(1)  

# Drop irrelevant or problematic columns if they exist
if 'Unnamed: 10' in df.columns:
    df = df.drop(columns=['Unnamed: 10'])

# Drop NaN values to avoid issues during training
df = df.dropna()

# Print dataset info after processing
print(f"Processed Data Shape: {df.shape}")
print(df.info())

# Define Features & Target
X = df[['surface Pressure', 'Humidity', 'Percipitation corrected', 'Wind speed', 
        'Irradiance wh/m^2', 'Prev_Temp', 'Prev_Humidity', 'Prev_WindSpeed', 'Prev_Irradiance']]
y = df['Temp at 2meter']

# Split into training (80%) and testing (20%) data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Initialize XGBoost Model
model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, objective='reg:squarederror')

# Train the Model
model.fit(X_train, y_train)

# Make Predictions
y_pred = model.predict(X_test)

# Evaluate the Model
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae:.2f}°C")

# Save the Model for Future Use
joblib.dump(model, "xgboost_weather_model.pkl")
print("Model saved as 'xgboost_weather_model.pkl'")

# Predict the Next Day's Temperature Using the Latest Available Data
latest_data = X.iloc[-1:].values  # Get the most recent row
next_day_prediction = model.predict(latest_data)
print(f"Predicted Temperature for Next Day: {next_day_prediction[0]:.2f}°C")
