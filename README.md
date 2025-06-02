# Agriculture de précision : pipeline MLOps de bout en bout

Trois modèles de Machine Learning qui aident un exploitant agricole à décider pour chaque parcelle, et toute la chaîne MLOps qui les entoure : prétraitement, suivi des expériences avec MLflow, API FastAPI, interface Streamlit, tests, conteneurisation Docker et CI/CD GitHub Actions.

| Question posée | Modèle | Type |
|---|---|---|
| Quel **rendement** attendre (t/ha) ? | `random_forest_model.pkl` | Régression |
| Faut-il **irriguer** la parcelle ? | `random_forest_irrigation.pkl` | Classification |
| Faut-il **apporter de l'engrais** ? | `random_forest_fertilizer.pkl` | Classification |

**Résultat clé :** le modèle de rendement atteint **R² = 0,907** (MSE = 0,27) sur le jeu de test.

---

## Architecture

```
 Données brutes (~1 M de parcelles)
        │
        ▼
 Prétraitement ──► nettoyage, suppression des rendements négatifs,
 (src/data)        encodage one-hot (région, sol, culture, météo)
        │
        ▼
 Entraînement ───► Random Forest (régression ou classification selon la cible)
 (src/models)      suivi des métriques, paramètres et artefacts dans MLflow
        │
        ▼
 API FastAPI ────► POST /predict/ : rendement, irrigation, fertilisation
 (src/api)         (au choix, dans une seule requête)
        │
        ▼
 Interface ──────► Streamlit : l'exploitant saisit sa parcelle et obtient les prédictions
 (scripts/)
```

## Les données

Environ **1 million de parcelles** (999 769 lignes après nettoyage), décrites par :
- **Climat** : pluviométrie (mm), température (°C), conditions météo (ensoleillé, nuageux, pluvieux)
- **Terrain** : région (Nord, Sud, Est, Ouest), type de sol (argileux, sableux, limoneux, crayeux, tourbeux, silteux)
- **Culture** : blé, maïs, riz, orge, soja, coton
- **Pratiques** : irrigation, engrais, nombre de jours avant la récolte
- **Cible** : rendement en tonnes par hectare

Le jeu complet n'est pas versionné, pour garder le dépôt léger. Un échantillon de 100 lignes ([`data/processed/sample_data.csv`](data/processed/sample_data.csv)) permet de faire tourner les tests et la CI.

## Ce que le projet met en pratique

- **Reproductibilité** : configuration centralisée (`config/`), scripts d'entraînement paramétrés, dépendances figées dans `requirements.txt`.
- **Suivi des expériences** : chaque entraînement est enregistré dans **MLflow** (métriques MSE/R² ou accuracy/F1, hyperparamètres, modèle sérialisé).
- **Service de prédiction** : API **FastAPI** avec validation des entrées par **Pydantic**. Une seule route calcule une, deux ou trois prédictions.
- **Tests** : `pytest` couvre le chargement des données, les modèles et l'API (via `TestClient`).
- **CI/CD** : à chaque push, **GitHub Actions** installe l'environnement et lance les tests. Sur `main`, l'image Docker de l'API est construite et publiée sur Docker Hub.
- **Conteneurisation** : `Dockerfile` et `docker-compose.yml` pour lancer l'API en une commande.

## Structure

```
├── config/                  # config.yaml, model_config.yaml
├── data/processed/          # Échantillon pour les tests et la CI
├── notebooks/               # 01 exploration · 02 prétraitement · 03 entraînement · 04 évaluation
├── src/
│   ├── data/                # Chargement et prétraitement
│   ├── models/              # Entraînement + modèles entraînés (.pkl)
│   └── api/                 # API FastAPI
├── scripts/                 # Lanceurs (prétraitement, entraînement, API) + app Streamlit
├── tests/                   # Tests des données, des modèles et de l'API
├── docker/                  # Dockerfile, docker-compose.yml
└── .github/workflows/ci.yml # Intégration et déploiement continus
```

## Démarrage rapide

```bash
git clone https://github.com/adononcarlos/Projet_Mlops.git
cd Projet_Mlops
pip install -r requirements.txt
```

**Lancer les tests :**
```bash
PYTHONPATH=. pytest tests/
```

**Démarrer l'API** (http://localhost:8000/docs) :
```bash
uvicorn src.api.main:app --reload
# ou avec Docker
cd docker && docker compose up --build
```

**Démarrer l'interface** (http://localhost:8501, l'API doit tourner) :
```bash
streamlit run scripts/app_streamlit.py
```

**Réentraîner un modèle avec suivi MLflow :**
```bash
mlflow ui                                # http://localhost:5000
python scripts/run_training.py           # rendement
python scripts/run_training_irrigation.py
python scripts/run_training_fertilizer.py
```

**Exemple d'appel à l'API :**
```bash
curl -X POST "http://localhost:8000/predict/" -H "Content-Type: application/json" \
  -d '{"Rainfall_mm": 500, "Temperature_Celsius": 25, "Fertilizer_Used": 1, "Irrigation_Used": 0,
       "Days_to_Harvest": 100, "Yield_tons_per_hectare": 0, "Region_East": 1, "Region_North": 0,
       "Region_South": 0, "Region_West": 0, "Soil_Type_Chalky": 0, "Soil_Type_Clay": 1,
       "Soil_Type_Loam": 0, "Soil_Type_Peaty": 0, "Soil_Type_Sandy": 0, "Soil_Type_Silt": 0,
       "Crop_Barley": 0, "Crop_Cotton": 0, "Crop_Maize": 1, "Crop_Rice": 0, "Crop_Soybean": 0,
       "Crop_Wheat": 0, "Weather_Condition_Cloudy": 0, "Weather_Condition_Rainy": 0,
       "Weather_Condition_Sunny": 1}'
```

## Pistes d'évolution

- Monitoring des modèles en production (Prometheus / Grafana) et détection de dérive des données
- Registre de modèles MLflow pour promouvoir une version en production
- Déploiement cloud de l'API et de l'interface

## Stack

Python 3.11 · scikit-learn · pandas · MLflow · FastAPI · Pydantic · Streamlit · pytest · Docker · GitHub Actions

## Auteur

**Franès Carlos ADONON** · [github.com/adononcarlos](https://github.com/adononcarlos)
