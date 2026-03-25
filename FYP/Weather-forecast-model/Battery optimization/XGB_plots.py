import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import style

# Set style for plots
style.use('ggplot')
plt.rcParams['figure.figsize'] = (12, 6)

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
#       Visualization Section
# =============================

# 1. Feature Importance Plot
# plt.figure(figsize=(10, 6))
# feature_importance = model.feature_importances_
# sorted_idx = np.argsort(feature_importance)
# pos = np.arange(sorted_idx.shape[0]) + 0.5
# 
# plt.barh(pos, feature_importance[sorted_idx], align='center')
# plt.yticks(pos, np.array(X.columns)[sorted_idx])
# plt.xlabel('Feature Importance Score')
# plt.title('XGBoost Feature Importance')
# plt.tight_layout()
# plt.savefig('feature_importance.png', dpi=300)
# plt.show()

# 2. Actual vs Predicted Values Scatter Plot
# plt.figure(figsize=(10, 6))
# plt.scatter(y_test, y_pred, alpha=0.5)
# plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)
# plt.xlabel('Actual Irradiance (Wh/m²)')
# plt.ylabel('Predicted Irradiance (Wh/m²)')
# plt.title('Actual vs Predicted Irradiance')
# plt.grid(True)
# plt.savefig('actual_vs_predicted.png', dpi=300)
# plt.show()

# 3. Time Series Comparison Plot (first 100 samples for clarity)
# test_dates = df['Datetime'].iloc[-len(y_test):]
# plt.figure(figsize=(14, 7))
# plt.plot(test_dates[:200], y_test.values[:200], label='Actual', marker='o')
# plt.plot(test_dates[:200], y_pred[:200], label='Predicted', marker='x')
# plt.xlabel('Date')
# plt.ylabel('Irradiance (Wh/m²)')
# plt.title('Time Series: Actual vs Predicted Irradiance (First 200 Samples)')
# plt.legend()
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.savefig('time_series_comparison.png', dpi=300)
# plt.show()

# 4. Error Distribution Plot
# errors = y_test - y_pred
# plt.figure(figsize=(10, 6))
# sns.histplot(errors, kde=True, bins=30)
# plt.xlabel('Prediction Error (Wh/m²)')
# plt.ylabel('Frequency')
# plt.title('Distribution of Prediction Errors')
# plt.axvline(x=0, color='r', linestyle='--')
# plt.savefig('error_distribution.png', dpi=300)
# plt.show()

# 5. Confusion Matrix for Classification
cm = confusion_matrix(y_test_class, y_pred_class)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Not Sunny', 'Sunny'], 
            yticklabels=['Not Sunny', 'Sunny'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix (Threshold = 500 Wh/m²)')
plt.savefig('confusion_matrix.png', dpi=300)
plt.show()

# 6. Feature Correlation Heatmap
plt.figure(figsize=(12, 8))
corr_matrix = X.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Feature Correlation Heatmap')
plt.tight_layout()
plt.savefig('feature_correlation.png', dpi=300)
plt.show()

# =============================
#       Save the Model
# =============================
joblib.dump(model, "xgboost_irradiance_model.pkl")
print("\nModel saved as 'xgboost_irradiance_model.pkl'")