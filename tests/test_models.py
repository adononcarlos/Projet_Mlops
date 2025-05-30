import joblib
import pandas as pd
import numpy as np

# Charger le modèle
model = joblib.load('models/random_forest_model.pkl')

# Exemple de données (à adapter selon vos features)
example_data = {
    'Region': 0,  # Encodé
    'Temperature': 25.0,
    'Humidity': 65.0,
    'Rainfall': 1000.0,
    'Soil_Type': 1,  # Encodé
    'Crop': 0,  # Encodé
    'Weather_Condition': 1,  # Encodé
    'Fertilizer_Used': 1,  # 0 ou 1
    'Irrigation_Used': 1,  # 0 ou 1
}

# Convertir en DataFrame
input_data = pd.DataFrame([example_data])

# Faire une prédiction
prediction = model.predict(input_data)

print(f"\nPour les conditions suivantes :")
for feature, value in example_data.items():
    print(f"{feature}: {value}")
print(f"\nRendement prédit : {prediction[0]:.2f} tonnes par hectare")