import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, f1_score
import joblib
import mlflow
import mlflow.sklearn
from src.config import get_data_path  # AJOUTER CETTE LIGNE

mlflow.set_tracking_uri("http://127.0.0.1:5000")


def train_model(data_path: str = None, model_path: str = "", target_column: str = "") -> dict:
    """
    Entraîne un modèle Random Forest adapté à la tâche (régression ou classification) selon la colonne cible.
    Loggue le modèle et les métriques dans MLflow.
    """
    try:
        if data_path is None:
            data_path = get_data_path()  # Utilise le chemin dynamique si non fourni

        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Le fichier {data_path} n’existe pas.")

        df = pd.read_csv(data_path)

        if target_column not in df.columns:
            raise KeyError(f"La colonne '{target_column}' est manquante dans le DataFrame.")

        X = df.drop(target_column, axis=1)
        y = df[target_column]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Choix du modèle selon la nature de la cible
        if y.nunique() > 10 and y.dtype != 'O':  # Régression si beaucoup de valeurs différentes
            model = RandomForestRegressor(n_estimators=30, max_depth=8, random_state=42)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            metrics = {'mse': mse, 'r2': r2}
            run_name = f"RandomForestRegressor_{target_column}"
        else:  # Classification sinon
            model = RandomForestClassifier(n_estimators=30, max_depth=8, random_state=42)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            metrics = {'accuracy': accuracy, 'f1': f1}
            run_name = f"RandomForestClassifier_{target_column}"

        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump(model, model_path)

        # --- MLflow logging ---
        with mlflow.start_run(run_name=run_name):
            mlflow.sklearn.log_model(model, "model")
            mlflow.log_param("target_column", target_column)
            mlflow.log_param("model_path", model_path)
            for k, v in metrics.items():
                mlflow.log_metric(k, v)

        return metrics

    except Exception as e:
        raise Exception(f"Erreur lors de l'entraînement du modèle : {e}")