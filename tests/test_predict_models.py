import pandas as pd
import joblib
import os

# Charger un échantillon de données prétraitées
data_path = 'data/processed/cleaned_data.csv'
df = pd.read_csv(data_path)

# Prendre la première ligne comme exemple
sample = df.iloc[[0]].copy()

# Prédiction du rendement
model_yield = joblib.load('src/models/random_forest_model.pkl')
yield_pred = model_yield.predict(sample.drop('Yield_tons_per_hectare', axis=1))
print(f"Prédiction rendement (Yield): {yield_pred[0]}")

# Prédiction irrigation
model_irrig = joblib.load('src/models/random_forest_irrigation.pkl')
irrig_pred = model_irrig.predict(sample.drop('Irrigation_Used', axis=1))
print(f"Prédiction irrigation (Irrigation_Used): {irrig_pred[0]}")

# Prédiction fertilisation
model_fert = joblib.load('src/models/random_forest_fertilizer.pkl')
fert_pred = model_fert.predict(sample.drop('Fertilizer_Used', axis=1))
print(f"Prédiction fertilisation (Fertilizer_Used): {fert_pred[0]}")