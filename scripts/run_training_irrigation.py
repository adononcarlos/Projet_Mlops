import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.train_model import train_model

data_path = 'data/processed/cleaned_data.csv'
model_path = 'src/models/random_forest_irrigation.pkl'
target_column = 'Irrigation_Used'

metrics = train_model(data_path, model_path, target_column)
print(f"Modèle irrigation entraîné. Accuracy: {metrics['accuracy']:.4f}, F1: {metrics['f1']:.4f}")