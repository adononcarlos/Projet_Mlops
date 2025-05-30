import joblib
import pandas as pd
import numpy as np
import os

# Définir le chemin correct vers le modèle
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src', 'models', 'random_forest_model.pkl')

print(f"Chemin du modèle : {MODEL_PATH}")

# Vérifier si le modèle existe
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Le modèle n'existe pas au chemin : {MODEL_PATH}")
else:
    print("Le modèle a été trouvé !")

try:
    # Charger le modèle
    print("Chargement du modèle...")
    model = joblib.load(MODEL_PATH)
    print("Modèle chargé avec succès !")

    # Exemple de données avec toutes les features du modèle
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
    print("\nDonnées d'entrée :")
    print(input_data)

    # Faire une prédiction
    print("\nPrédiction en cours...")
    prediction = model.predict(input_data)

    print(f"\nPour les conditions suivantes :")
    for feature, value in example_data.items():
        print(f"{feature}: {value}")
    print(f"\nRendement prédit : {prediction[0]:.2f} tonnes par hectare")

except Exception as e:
    print(f"Une erreur s'est produite : {str(e)}") 