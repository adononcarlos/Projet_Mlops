# Projet MLOps - Optimisation Agricole

![CI](https://github.com/adononcarlos/Projet_Mlops/actions/workflows/ci.yml/badge.svg)

## Présentation

Ce projet vise à optimiser les rendements agricoles grâce au Machine Learning, en appliquant les bonnes pratiques MLOps : automatisation, reproductibilité, CI/CD, gestion des dépendances, versioning des modèles et interface utilisateur.

---

## Fonctionnalités et avancement

- **Prétraitement des données**  
  - Suppression des valeurs négatives
  - Encodage des variables catégoriques
  - Exploration des données dans `notebooks/01_data_exploration.ipynb` (visualisations, corrélations)

- **Modélisation et versioning**  
  - Entraînement de trois modèles Random Forest :
    - **Modèle de rendement (`random_forest_model.pkl`)**  
      Prédit le rendement agricole (`Yield_tons_per_hectare`) à partir des caractéristiques d'entrée.  
      *Emplacement :* `src/models/random_forest_model.pkl`
    - **Modèle d'irrigation (`random_forest_irrigation.pkl`)**  
      Prédit si une parcelle doit être irriguée (`Irrigation_Used`).  
      *Emplacement :* `src/models/random_forest_irrigation.pkl`
    - **Modèle de fertilisation (`random_forest_fertilizer.pkl`)**  
      Prédit si une parcelle nécessite de l'engrais (`Fertilizer_Used`).  
      *Emplacement :* `src/models/random_forest_fertilizer.pkl`
  - Script d’entraînement automatisé dans `src/models/train_model.py`
  - **Versioning et suivi des modèles avec MLflow**  
    - Chaque entraînement est tracé (métriques, hyperparamètres, artefacts)  
    - Visualisation via l’interface MLflow

- **API de prédiction (FastAPI)**  
  - Expose les modèles via une API REST (`src/api/main.py`)
  - Prédiction du rendement, de l’irrigation et de la fertilisation via `/predict/`
  - Testée automatiquement avec `pytest` et `TestClient`

- **Interface utilisateur (Streamlit)**  
  - Application Streamlit dans `scripts/app_streamlit.py`
  - Permet à l’utilisateur de saisir les paramètres de la parcelle et d’obtenir des prédictions en appelant l’API

- **CI/CD et automatisation**  
  - Workflow GitHub Actions pour l’intégration continue (CI) :  
    - Installation des dépendances
    - Exécution automatique des tests à chaque push/pull request
    - Build et push automatisé de l’image Docker sur Docker Hub (CD)
    - Badge de statut CI dans ce README

- **Gestion des données et du dépôt**  
  - `.gitignore` adapté pour ignorer les gros fichiers/datasets et les environnements virtuels
  - Ajout d’un petit dataset de test (`sample_data.csv`) pour la CI
  - Nettoyage de l’historique Git pour supprimer les fichiers trop volumineux

---

## Structure du projet

```
├── data/
│   └── processed/
│       └── sample_data.csv
├── notebooks/
├── src/
│   ├── config.py
│   └── models/
│       ├── train_model.py
│       ├── random_forest_model.pkl
│       ├── random_forest_irrigation.pkl
│       └── random_forest_fertilizer.pkl
│   └── api/
│       └── main.py
├── scripts/
│   └── app_streamlit.py
├── tests/
│   ├── test_api.py
│   └── test_predict_models.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .github/
│   └── workflows/
│       └── ci.yml
├── requirements.txt
└── README.md
```

---

## Instructions d’utilisation

### 1. **Installer les dépendances**

```sh
pip install -r requirements.txt
```

---

### 2. **Lancer les tests en local**

```sh
pytest
```

---

### 3. **Entraîner et versionner les modèles avec MLflow**

- Lancer le serveur MLflow (pour visualiser les runs) :
  ```sh
  mlflow ui
  ```
  Accéder à [http://localhost:5000](http://localhost:5000)

- Entraîner un modèle et logger dans MLflow :
  ```python
  from src.models.train_model import train_model
  train_model(
      data_path="data/processed/cleaned_data.csv",
      model_path="src/models/random_forest_model.pkl",
      target_column="Yield_tons_per_hectare"
  )
  ```

---

### 4. **Lancer l’API en local**

- Avec Uvicorn :
  ```sh
  uvicorn src.api.main:app --reload
  ```
- Ou avec Docker Compose :
  ```sh
  cd docker
  docker-compose up --build
  ```

---

### 5. **Lancer l’interface utilisateur Streamlit**

```sh
streamlit run scripts/app_streamlit.py
```
- L’interface est accessible sur [http://localhost:8501](http://localhost:8501)
- ⚠️ L’API FastAPI doit être lancée pour que l’interface fonctionne.

---

### 6. **Visualiser et suivre les modèles avec MLflow**

- Accéder à [http://localhost:5000](http://localhost:5000) pour voir les runs, métriques, et artefacts.

---

## Prochaines étapes possibles

- Ajouter d’autres tests unitaires et d’intégration
- Déploiement de l’API (Docker, cloud…)
- Monitoring et suivi avancé des modèles
- Documentation détaillée des endpoints et des scripts

---

## Auteur

Franès ADONON