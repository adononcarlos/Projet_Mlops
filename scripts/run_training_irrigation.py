import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.train_model import train_model

from src.config import get_data_path  # AJOUTER CETTE LIGNE

# Charger un échantillon de données prétraitées
data_path = get_data_path()  # MODIFIER CETTE LIGNE
model_path = 'src/models/random_forest_irrigation.pkl'
target_column = 'Irrigation_Used'

metrics = train_model(data_path, model_path, target_column)
print(f"Modèle irrigation entraîné. Accuracy: {metrics['accuracy']:.4f}, F1: {metrics['f1']:.4f}")