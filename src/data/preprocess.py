import pandas as pd
import pickle

def preprocess_data(df: pd.DataFrame, encoders_path: str = 'src/data/encoders.pkl') -> pd.DataFrame:
    """
    Nettoie et prétraite les données.
    
    Args:
        df (pd.DataFrame): DataFrame brut contenant les données.
        encoders_path (str): Chemin pour sauvegarder les colonnes one-hot.
    
    Returns:
        pd.DataFrame: DataFrame prétraité avec toutes les colonnes, y compris la cible.
    
    Raises:
        KeyError: Si une colonne attendue est manquante.
        Exception: Pour toute autre erreur lors du prétraitement.
    """
    try:
        # Vérifier que toutes les colonnes attendues sont présentes
        expected_columns = [
            'Region', 'Soil_Type', 'Crop', 'Rainfall_mm', 'Temperature_Celsius',
            'Fertilizer_Used', 'Irrigation_Used', 'Weather_Condition', 'Days_to_Harvest',
            'Yield_tons_per_hectare'
        ]
        missing_cols = [col for col in expected_columns if col not in df.columns]
        if missing_cols:
            raise KeyError(f"Colonnes manquantes : {missing_cols}")

        # Copier le DataFrame pour éviter de modifier l'original
        df_clean = df.copy()

        # Supprimer les valeurs manquantes
        df_clean = df_clean.dropna()

        # Supprimer les lignes avec Yield_tons_per_hectare négatif
        df_clean = df_clean[df_clean['Yield_tons_per_hectare'] >= 0]

        # Encoder les variables catégoriques avec one-hot encoding
        categorical_columns = ['Region', 'Soil_Type', 'Crop', 'Weather_Condition']
        df_clean = pd.get_dummies(df_clean, columns=categorical_columns, prefix=categorical_columns, dtype=int)

        # S'assurer que les colonnes booléennes sont en 0/1
        df_clean['Fertilizer_Used'] = df_clean['Fertilizer_Used'].astype(int)
        df_clean['Irrigation_Used'] = df_clean['Irrigation_Used'].astype(int)

        # Sauvegarder les colonnes du DataFrame prétraité pour une utilisation future
        with open(encoders_path, 'wb') as f:
            pickle.dump(df_clean.columns.tolist(), f)

        return df_clean

    except Exception as e:
        raise Exception(f"Erreur lors du prétraitement des données : {e}")