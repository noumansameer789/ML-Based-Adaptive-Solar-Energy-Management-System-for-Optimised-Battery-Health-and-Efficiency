# =============================
#       Import Libraries
# =============================
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

# =============================
#       Load Dataset
# =============================
df = pd.read_csv("D:/Uni/FYP/Weather-forecast-model/Battery optimization/weather_data1.csv", encoding='latin1')
print(f"Initial Data Shape: {df.shape}")
df.rename(columns=lambda x: x.strip(), inplace=True)
df.rename(columns={'YEAR': 'year', 'MO': 'month', 'DY': 'day', 'HR': 'hour'}, inplace=True)
df['Datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']], errors='coerce')
df = df.sort_values(by='Datetime')

# =============================
#       Feature Engineering
# =============================
df['Prev_Temp'] = df['Temp at 2meter'].shift(1)  
df['Prev_Humidity'] = df['Humidity'].shift(1)  
df['Prev_WindSpeed'] = df['Wind speed'].shift(1)  
df['Prev_Irradiance'] = df['Irradiance wh/m^2'].shift(1)  

# Drop unnecessary columns and NaNs
if 'Unnamed: 10' in df.columns:
    df = df.drop(columns=['Unnamed: 10'])
df.replace(-999.0, np.nan, inplace=True)
df.dropna(inplace=True)

print(f"Processed Data Shape: {df.shape}")

# =============================
#       Feature Selection
# =============================
X = df[['surface Pressure', 'Humidity', 'Percipitation corrected', 'Wind speed', 
        'Temp at 2meter', 'Prev_Temp', 'Prev_Humidity', 'Prev_WindSpeed', 'Prev_Irradiance']]
y = df['Irradiance wh/m^2']

# =============================
#       Train-Test Split
# =============================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# =============================
#       Model Training
# =============================
model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, objective='reg:squarederror')
model.fit(X_train, y_train)

# =============================
#       Prediction
# =============================
y_pred = model.predict(X_test)

# =============================
#       Evaluation Metrics
# =============================
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n📝 Evaluation Metrics:")
print(f"Mean Absolute Error (MAE): {mae:.2f} Wh/m²")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f} Wh/m²")
print(f"R² Score (Coefficient of Determination): {r2:.2f}")

# =============================
#       Classification Metrics (Threshold-Based)
# =============================
# Let's choose a threshold, say 100 Wh/m² to classify "Sunny" vs "Not Sunny"
threshold = 500
y_test_class = (y_test > threshold).astype(int)
y_pred_class = (y_pred > threshold).astype(int)

accuracy = accuracy_score(y_test_class, y_pred_class)
precision = precision_score(y_test_class, y_pred_class)
recall = recall_score(y_test_class, y_pred_class)
f1 = f1_score(y_test_class, y_pred_class)

print("\n🔎 Classification Metrics (Threshold = 500 Wh/m²):")
print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")

# =============================
#       Save the Model
# =============================
joblib.dump(model, "xgboost_irradiance_model.pkl")
print("Model saved as 'xgboost_irradiance_model.pkl'")
