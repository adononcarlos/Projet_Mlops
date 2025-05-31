# Projet MLOps - Optimisation Agricole

![CI](https://github.com/adononcarlos/Projet_Mlops/actions/workflows/ci.yml/badge.svg)

## Présentation

Ce projet vise à optimiser les rendements agricoles grâce au Machine Learning, en appliquant les bonnes pratiques MLOps : automatisation, reproductibilité, CI/CD, gestion des dépendances et des données.

---

## Fonctionnalités et avancement

- **Prétraitement des données**  
  - Suppression des valeurs négatives
  - Encodage des variables catégoriques
  - Exploration des données dans `notebooks/01_data_exploration.ipynb` (visualisations, corrélations)
- **Modélisation**  
  - Entraînement d’un premier modèle Random Forest dans `notebooks/03_model_training.ipynb`
  - Script d’entraînement automatisé dans `src/models/train_model.py`
- **Gestion des chemins de données**  
  - Fonction centrale `get_data_path` dans `src/config.py` :  
    Utilise automatiquement `data/processed/cleaned_data.csv` s’il existe, sinon `data/processed/sample_data.csv` (pour la CI)
- **Tests et CI/CD**  
  - Tests unitaires et d’API avec `pytest`
  - Utilisation de `TestClient` pour tester l’API FastAPI sans serveur externe
  - Workflow GitHub Actions pour l’intégration continue (CI) :  
    - Installation des dépendances
    - Exécution automatique des tests à chaque push/pull request
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
│       └── train_model.py
│   └── api/
│       └── main.py
├── tests/
│   ├── test_api.py
│   └── test_predict_models.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── requirements.txt
└── README.md
```

---

## Prochaines étapes possibles

- Ajouter d’autres tests unitaires et d’intégration
- Déploiement de l’API (Docker, cloud…)
- Monitoring et suivi des modèles
- Documentation détaillée des endpoints et des scripts

---

## Lancer les tests en local

```sh
pytest
```

---

## Lancer l’API en local

```sh
uvicorn src.api.main:app --reload
```

---

## Auteur

Franès ADONON