import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

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
df.dropna(inplace=True)

# Replace -999.0 values (invalid placeholders) with NaN
df.replace(-999.0, np.nan, inplace=True)

# Drop rows with NaNs after replacement
df.dropna(inplace=True)

# Print dataset info after processing
print(f"Processed Data Shape: {df.shape}")
print(df.info())

print("Max Irradiance:", df['Irradiance wh/m^2'].max())
print("Min Irradiance:", df['Irradiance wh/m^2'].min())
print("Mean Irradiance:", df['Irradiance wh/m^2'].mean())

# Define Features & Target (Predicting Next Day's Irradiance)
X = df[['surface Pressure', 'Humidity', 'Percipitation corrected', 'Wind speed', 
        'Temp at 2meter', 'Prev_Temp', 'Prev_Humidity', 'Prev_WindSpeed', 'Prev_Irradiance']]
y = df['Irradiance wh/m^2']

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
print(f"Mean Absolute Error: {mae:.2f} Wh/m²")

# -------------------------------
# Predicted vs Actual Scatter Plot
# -------------------------------
plt.figure(figsize=(6, 6))
plt.scatter(y_test, y_pred, alpha=0.5, color='blue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--', color='red')
plt.xlabel("Actual Irradiance (Wh/m²)")
plt.ylabel("Predicted Irradiance (Wh/m²)")
plt.title("Predicted vs Actual Irradiance")
plt.grid(True)
plt.tight_layout()
plt.show()

# -------------------------------
# Residuals Plot (Errors)
# -------------------------------
residuals = y_test - y_pred
plt.figure(figsize=(10, 4))
plt.plot(residuals.values, marker='o', linestyle='', alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.title("Residual Plot")
plt.ylabel("Prediction Error (Wh/m²)")
plt.xlabel("Test Sample Index")
plt.tight_layout()
plt.show()

# -------------------------------
# Histogram of Residuals
# -------------------------------
plt.figure(figsize=(8, 4))
plt.hist(residuals, bins=50, color='green', alpha=0.7)
plt.title("Distribution of Prediction Errors")
plt.xlabel("Error (Wh/m²)")
plt.ylabel("Frequency")
plt.grid(True)
plt.tight_layout()
plt.show()

# -------------------------------
# Line Plot: Actual vs Predicted (Trend Over Time)
# -------------------------------
plt.figure(figsize=(12, 5))
plt.plot(y_test.values[:200], label='Actual', marker='o')  # Plot first 200 for clarity
plt.plot(y_pred[:200], label='Predicted', marker='x')
plt.title("Actual vs Predicted Irradiance (First 200 Samples)")
plt.xlabel("Time Step")
plt.ylabel("Irradiance (Wh/m²)")
plt.legend()
plt.tight_layout()
plt.savefig('time_series_comparison.png', dpi=300)
plt.show()

# -------------------------------
# R² Score
# -------------------------------
r2 = r2_score(y_test, y_pred)
print(f"R² Score: {r2:.3f}")

# Save the Model for Future Use
joblib.dump(model, "xgboost_irradiance_model.pkl")
print("Model saved as 'xgboost_irradiance_model.pkl'")

# Manual Input for Current Day Parameters
print("Enter current weather conditions:")
current_temp = float(input("Temperature at 2m (°C): "))
current_humidity = float(input("Humidity (%): "))
current_pressure = float(input("Surface Pressure (hPa): "))
current_wind_speed = float(input("Wind Speed (m/s): "))
current_precipitation = float(input("Precipitation (mm): "))
prev_irradiance = float(input("Previous Day Irradiance (Wh/m²): "))

# Create a DataFrame with the user inputs
manual_input = pd.DataFrame([[current_pressure, current_humidity, current_precipitation, 
                              current_wind_speed, current_temp, current_temp, 
                              current_humidity, current_wind_speed, prev_irradiance]], 
                            columns=X.columns)

# Load the trained model and make predictions
model = joblib.load("xgboost_irradiance_model.pkl")
next_day_irradiance = model.predict(manual_input)
print(f"Predicted Solar Irradiance for Next Day: {next_day_irradiance[0]:.2f} Wh/m²")