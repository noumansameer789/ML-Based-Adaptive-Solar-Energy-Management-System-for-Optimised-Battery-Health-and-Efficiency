# ML-Based Adaptive Solar Energy Management System for Optimised Battery Health and Efficiency

## Overview
This project presents an ML-based adaptive solar energy management system designed to improve battery health, charging efficiency, and overall solar power utilization. The system combines machine learning, real-time sensor monitoring, and embedded control to predict solar irradiance and optimize battery charging/discharging decisions under varying environmental conditions.

The project is built around a Raspberry Pi and supporting hardware sensors, with an XGBoost-based prediction model used to estimate solar irradiance from weather-related inputs.

## Objectives
- Predict solar irradiance using machine learning
- Improve battery charging and discharging efficiency
- Extend lithium-ion battery health and lifecycle
- Monitor environmental and electrical parameters in real time
- Provide a scalable and cost-effective solution for smart solar systems

## Features
- Solar irradiance prediction using XGBoost and Random Forest models
- Real-time sensor integration for environmental monitoring
- Battery state monitoring and optimization
- Hardware prototype for practical deployment
- Data visualization and model evaluation plots
- Weather-based adaptive energy management

## Project Structure
```text
FYP/
│
├── Weather-forecast-model/
│   └── Battery optimization/
│       ├── xgboost_model.py
│       ├── xgboost_modelv2.py
│       ├── xgboost_modelv3.py
│       ├── random_forest.py
│       ├── weather_data1.csv
│       ├── xgboost_irradiance_model.pkl
│       └── evaluation plots
│
├── soc circuit/
│   ├── Proteus/project files
│   ├── Arduino code
│   └── simulation screenshots
│
├── Hardware imgs/
│   ├── sensor images
│   ├── prototype images
│   └── battery parameter screenshots

Technologies Used
Python
XGBoost
Random Forest
Raspberry Pi
Arduino/ESP32
Firebase
CSV/XLSX weather datasets
Embedded sensors for temperature, humidity, rain, light, and battery monitoring
Machine Learning Models

This project includes:

XGBoost model for solar irradiance prediction
Random Forest model for comparison and evaluation

The models are trained using weather-related input data and evaluated using prediction plots, error analysis, feature importance, and time-series comparisons.

Hardware Components

The hardware side of the project includes:

Raspberry Pi
Battery Management System (BMS)
Temperature and humidity sensor
Rain sensor
Light sensor / LDR
Anemometer
SOC monitoring circuitry
Prototype circuit setup
Use Cases
Smart solar charging systems
Battery-aware renewable energy management
Off-grid solar applications
Low-cost intelligent power systems
Academic and research-based embedded ML projects
Results

The project demonstrates how machine learning can be integrated with embedded hardware to:

predict solar conditions more effectively,
adapt charging behavior,
reduce battery stress,
and improve long-term energy management performance.
Future Improvements
Deploy model directly on edge hardware for real-time inference
Add more environmental features for better accuracy
Improve dashboard/visualization for live monitoring
Integrate cloud-based logging and analytics
Expand support for larger solar storage systems

Author
Nouman Sameer

## License

All rights reserved.

This project is shared for viewing and academic reference only. No permission is granted to copy, modify, distribute, or reuse any part of this work without explicit written permission from the author.

This project is for academic and educational purposes.

Notes

Some large files and generated assets may be excluded from version control using .gitignore and Git LFS where needed.
