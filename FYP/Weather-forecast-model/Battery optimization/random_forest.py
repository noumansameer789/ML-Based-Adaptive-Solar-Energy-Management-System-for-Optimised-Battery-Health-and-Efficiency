import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# Load dataset
df = pd.read_csv("D:/Uni/FYP/Weather-forecast-model/Battery optimization/weather_data1.csv", encoding='latin1')

# Clean column names
df.rename(columns=lambda x: x.strip(), inplace=True)
df.rename(columns={'YEAR': 'year', 'MO': 'month', 'DY': 'day', 'HR': 'hour'}, inplace=True)

# Create datetime column
df['Datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']], errors='coerce')
df = df.sort_values(by='Datetime')

# Create lag features
df['Prev_Temp'] = df['Temp at 2meter'].shift(1)
df['Prev_Humidity'] = df['Humidity'].shift(1)
df['Prev_WindSpeed'] = df['Wind speed'].shift(1)
df['Prev_Irradiance'] = df['Irradiance wh/m^2'].shift(1)

# Drop unnecessary columns and clean data
df = df.drop(columns=[col for col in df.columns if "Unnamed" in col], errors='ignore')
df.replace(-999.0, np.nan, inplace=True)
df.dropna(inplace=True)

# Define features and target
X = df[['surface Pressure', 'Humidity', 'Percipitation corrected', 'Wind speed',
        'Temp at 2meter', 'Prev_Temp', 'Prev_Humidity', 'Prev_WindSpeed', 'Prev_Irradiance']]
y = df['Irradiance wh/m^2']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Train Random Forest model
model = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluation Metrics
mae = mean_absolute_error(y_test, y_pred)
#rmse = mean_squared_error(y_test, y_pred, squared=False)  # RMSE
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

r2 = r2_score(y_test, y_pred)

print(f"\n📊 Evaluation Metrics:")
print(f"Mean Absolute Error (MAE): {mae:.2f} Wh/m²")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f} Wh/m²")
print(f"R² Score (Accuracy): {r2:.4f}")

# Save model
joblib.dump(model, "rf_irradiance_model.pkl")
print("\n✅ Model saved as 'rf_irradiance_model.pkl'")

# Manual input for next-day prediction
print("\n🔍 Enter current weather conditions:")
current_temp = float(input("Temperature at 2m (°C): "))
current_humidity = float(input("Humidity (%): "))
current_pressure = float(input("Surface Pressure (hPa): "))
current_wind_speed = float(input("Wind Speed (m/s): "))
current_precipitation = float(input("Precipitation (mm): "))
prev_irradiance = float(input("Previous Day Irradiance (Wh/m²): "))

# Prepare input
manual_input = pd.DataFrame([[current_pressure, current_humidity, current_precipitation,
                              current_wind_speed, current_temp, current_temp,
                              current_humidity, current_wind_speed, prev_irradiance]],
                            columns=X.columns)

# Load and predict
model = joblib.load("rf_irradiance_model.pkl")
next_day_irradiance = model.predict(manual_input)
print(f"\n🌞 Predicted Solar Irradiance for Next Day: {next_day_irradiance[0]:.2f} Wh/m²")
