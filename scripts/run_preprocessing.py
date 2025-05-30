import os
import sys
# Ajouter le répertoire racine du projet au chemin de recherche
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.load_data import load_data
from src.data.preprocess import preprocess_data

# Charger et prétraiter
df = load_data('data/raw/crop_yield.csv')
df_clean = preprocess_data(df)
df_clean.to_csv('data/processed/cleaned_data.csv', index=False)
print("Prétraitement terminé !")