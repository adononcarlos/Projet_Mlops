import streamlit as st
import requests

st.title("Prédiction Agriculture de Précision")

# Choix des prédictions à faire
pred_yield = st.checkbox("Prédire le rendement")
pred_irrig = st.checkbox("Prédire la nécessité d'irrigation")
pred_fert = st.checkbox("Prédire la nécessité de fertilisation")

# Colonnes du dataset
fields = [
    ("Rainfall_mm", st.number_input, {"label": "Rainfall (mm)", "min_value": 0.0}),
    ("Temperature_Celsius", st.number_input, {"label": "Temperature (°C)", "min_value": 0.0}),
    ("Fertilizer_Used", st.selectbox, {"label": "Fertilizer Used", "options": [0, 1]}),
    ("Irrigation_Used", st.selectbox, {"label": "Irrigation Used", "options": [0, 1]}),
    ("Days_to_Harvest", st.number_input, {"label": "Days to Harvest", "min_value": 0}),
    ("Yield_tons_per_hectare", st.number_input, {"label": "Yield (tons/ha)", "min_value": 0.0}),
    ("Region_East", st.selectbox, {"label": "Region East", "options": [0, 1]}),
    ("Region_North", st.selectbox, {"label": "Region North", "options": [0, 1]}),
    ("Region_South", st.selectbox, {"label": "Region South", "options": [0, 1]}),
    ("Region_West", st.selectbox, {"label": "Region West", "options": [0, 1]}),
    ("Soil_Type_Chalky", st.selectbox, {"label": "Soil Type Chalky", "options": [0, 1]}),
    ("Soil_Type_Clay", st.selectbox, {"label": "Soil Type Clay", "options": [0, 1]}),
    ("Soil_Type_Loam", st.selectbox, {"label": "Soil Type Loam", "options": [0, 1]}),
    ("Soil_Type_Peaty", st.selectbox, {"label": "Soil Type Peaty", "options": [0, 1]}),
    ("Soil_Type_Sandy", st.selectbox, {"label": "Soil Type Sandy", "options": [0, 1]}),
    ("Soil_Type_Silt", st.selectbox, {"label": "Soil Type Silt", "options": [0, 1]}),
    ("Crop_Barley", st.selectbox, {"label": "Crop Barley", "options": [0, 1]}),
    ("Crop_Cotton", st.selectbox, {"label": "Crop Cotton", "options": [0, 1]}),
    ("Crop_Maize", st.selectbox, {"label": "Crop Maize", "options": [0, 1]}),
    ("Crop_Rice", st.selectbox, {"label": "Crop Rice", "options": [0, 1]}),
    ("Crop_Soybean", st.selectbox, {"label": "Crop Soybean", "options": [0, 1]}),
    ("Crop_Wheat", st.selectbox, {"label": "Crop Wheat", "options": [0, 1]}),
    ("Weather_Condition_Cloudy", st.selectbox, {"label": "Weather Condition Cloudy", "options": [0, 1]}),
    ("Weather_Condition_Rainy", st.selectbox, {"label": "Weather Condition Rainy", "options": [0, 1]}),
    ("Weather_Condition_Sunny", st.selectbox, {"label": "Weather Condition Sunny", "options": [0, 1]}),
]

# Déterminer la colonne cible à exclure selon la prédiction
exclude = []
if pred_yield:
    exclude.append("Yield_tons_per_hectare")
if pred_irrig:
    exclude.append("Irrigation_Used")
if pred_fert:
    exclude.append("Fertilizer_Used")

# Saisie utilisateur (on n'affiche pas la colonne cible à prédire)
user_inputs = {}
for name, func, params in fields:
    # Si c'est la colonne cible, on met une valeur par défaut (0)
    if name in exclude:
        if func == st.number_input:
            user_inputs[name] = 0.0
        else:
            user_inputs[name] = 0
    else:
        user_inputs[name] = func(**params)

if st.button("Prédire"):
    # On envoie toutes les colonnes sauf la/les cibles à prédire
    data = user_inputs.copy()
    # On précise à l'API ce qu'on veut prédire
    params = {
        "predict_yield": pred_yield,
        "predict_irrig": pred_irrig,
        "predict_fert": pred_fert
    }
    try:
        response = requests.post("http://127.0.0.1:8000/predict/", params=params, json=data)
        if response.status_code == 200:
            result = response.json()
            if pred_yield and "yield_prediction" in result:
                st.success(f"Rendement prédit : {result['yield_prediction']}")
            if pred_irrig and "irrigation_prediction" in result:
                st.info(f"Irrigation nécessaire : {'Oui' if result['irrigation_prediction'] else 'Non'}")
            if pred_fert and "fertilizer_prediction" in result:
                st.info(f"Fertilisation nécessaire : {'Oui' if result['fertilizer_prediction'] else 'Non'}")
            if not (pred_yield or pred_irrig or pred_fert):
                st.warning("Coche au moins une case pour prédire.")
        else:
            st.error("Erreur lors de la prédiction.")
    except Exception as e:
        st.error(f"Erreur lors de la connexion à l'API : {e}")