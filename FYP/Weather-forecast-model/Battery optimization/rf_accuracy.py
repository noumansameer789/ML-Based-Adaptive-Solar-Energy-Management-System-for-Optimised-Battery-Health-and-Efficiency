import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error, 
    mean_squared_error, 
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)
import joblib
import matplotlib.pyplot as plt

# =============================
#       Load Dataset
# =============================
df = pd.read_csv("D:/Uni/FYP/Weather-forecast-model/Battery optimization/weather_data1.csv", encoding='latin1')
print(f"Initial Data Shape: {df.shape}")

# Clean column names
df.rename(columns=lambda x: x.strip(), inplace=True)
df.rename(columns={'YEAR': 'year', 'MO': 'month', 'DY': 'day', 'HR': 'hour'}, inplace=True)

# Create datetime column
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
df = df.drop(columns=[col for col in df.columns if "Unnamed" in col], errors='ignore')
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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False, random_state=42)

# =============================
#       Model Training (Random Forest)
# =============================
model = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42)
model.fit(X_train, y_train)

# =============================
#       Prediction
# =============================
y_pred = model.predict(X_test)

# =============================
#       Regression Metrics
# =============================
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n📊 Regression Metrics:")
print("=" * 40)
print(f"Mean Absolute Error (MAE): {mae:.2f} Wh/m²")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f} Wh/m²")
print(f"R² Score (Accuracy): {r2:.4f}")

# =============================
#       Classification Metrics (Threshold-Based)
# =============================
threshold = 500  # Define a threshold (adjust based on domain knowledge)
y_test_class = (y_test > threshold).astype(int)  # 1 if irradiance > threshold, else 0
y_pred_class = (y_pred > threshold).astype(int)  # Convert predictions to binary classes

# Compute metrics
accuracy = accuracy_score(y_test_class, y_pred_class)
precision = precision_score(y_test_class, y_pred_class, zero_division=0)
recall = recall_score(y_test_class, y_pred_class, zero_division=0)
f1 = f1_score(y_test_class, y_pred_class, zero_division=0)

print("\n🔍 Classification Metrics (Threshold = 500 Wh/m²):")
print("=" * 40)
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")

# Classification report
print("\n📝 Classification Report:")
print(classification_report(y_test_class, y_pred_class, zero_division=0))

# =============================
#       Save Model
# =============================
joblib.dump(model, "random_forest_irradiance_model.pkl")
print("\n✅ Model saved as 'random_forest_irradiance_model.pkl'")

# =============================
#       Feature Importance
# =============================
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\n🔝 Feature Importance:")
print(feature_importance.to_string(index=False))

# plt.hist(y, bins=50)
# plt.axvline(100, color='red', linestyle='--', label='Threshold (100 Wh/m²)')
# plt.xlabel('Irradiance (Wh/m²)')
# plt.ylabel('Frequency')
# plt.legend()
# plt.show()


plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.3)
plt.plot([0, max(y_test)], [0, max(y_test)], 'r--')  # Perfect prediction line
plt.xlabel("True Irradiance (Wh/m²)")
plt.ylabel("Predicted Irradiance (Wh/m²)")
plt.title("True vs. Predicted Irradiance")
plt.show()