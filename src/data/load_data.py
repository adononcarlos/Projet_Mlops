import pandas as pd

def load_data(file_path: str) -> pd.DataFrame:
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Le fichier {file_path} n’a pas été trouvé.")
    except Exception as e:
        raise Exception(f"Erreur lors du chargement des données : {e}")