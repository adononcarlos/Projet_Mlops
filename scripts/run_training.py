import os
import sys
# Ajouter le répertoire racine du projet au chemin de recherche
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.train_model import train_model

# Paramètres
data_path = 'data/processed/cleaned_data.csv'
model_path = 'src/models/random_forest_model.pkl'
target_column = 'Yield_tons_per_hectare'

# Entraîner
metrics = train_model(data_path, model_path, target_column)
print(f"Modèle entraîné. MSE: {metrics['mse']:.4f}, R²: {metrics['r2']:.4f}")