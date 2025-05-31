import os

def get_data_path():
    """
    Retourne le chemin du dataset à utiliser.
    Prend cleaned_data.csv s'il existe, sinon sample_data.csv.
    """
    full_path = "data/processed/cleaned_data.csv"
    sample_path = "data/processed/sample_data.csv"
    if os.path.exists(full_path):
        return full_path
    elif os.path.exists(sample_path):
        return sample_path
    else:
        raise FileNotFoundError("Aucun fichier de données trouvé.")