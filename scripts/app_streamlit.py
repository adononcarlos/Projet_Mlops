import streamlit as st
import requests

st.set_page_config(page_title="Prédiction Agriculture de Précision", page_icon="🌾")
st.image("https://cdn.pixabay.com/photo/2017/01/20/00/30/wheat-1995056_1280.jpg", width=120)
st.title("🌾 Prédiction Agriculture de Précision")

st.markdown("""
Bienvenue sur l'outil de prédiction agricole.<br>
Sélectionnez les paramètres de votre parcelle et choisissez les prédictions souhaitées.
""", unsafe_allow_html=True)

st.header("Sélection des prédictions")
col_pred1, col_pred2, col_pred3 = st.columns(3)
with col_pred1:
    pred_yield = st.checkbox("Prédire le rendement")
with col_pred2:
    pred_irrig = st.checkbox("Prédire l'irrigation")
with col_pred3:
    pred_fert = st.checkbox("Prédire la fertilisation")

st.divider()
st.header("Caractéristiques de la parcelle")

fields = [
    ("Rainfall_mm", st.number_input, {"label": "Pluviométrie (mm)", "min_value": 0.0}),
    ("Temperature_Celsius", st.number_input, {"label": "Température (°C)", "min_value": 0.0}),
    ("Fertilizer_Used", st.selectbox, {"label": "Engrais utilisé", "options": [0, 1]}),
    ("Irrigation_Used", st.selectbox, {"label": "Irrigation utilisée", "options": [0, 1]}),
    ("Days_to_Harvest", st.number_input, {"label": "Jours avant récolte", "min_value": 0}),
    ("Yield_tons_per_hectare", st.number_input, {"label": "Rendement (t/ha)", "min_value": 0.0}),
    ("Region_East", st.selectbox, {"label": "Région Est", "options": [0, 1]}),
    ("Region_North", st.selectbox, {"label": "Région Nord", "options": [0, 1]}),
    ("Region_South", st.selectbox, {"label": "Région Sud", "options": [0, 1]}),
    ("Region_West", st.selectbox, {"label": "Région Ouest", "options": [0, 1]}),
    ("Soil_Type_Chalky", st.selectbox, {"label": "Sol crayeux", "options": [0, 1]}),
    ("Soil_Type_Clay", st.selectbox, {"label": "Sol argileux", "options": [0, 1]}),
    ("Soil_Type_Loam", st.selectbox, {"label": "Sol limoneux", "options": [0, 1]}),
    ("Soil_Type_Peaty", st.selectbox, {"label": "Sol tourbeux", "options": [0, 1]}),
    ("Soil_Type_Sandy", st.selectbox, {"label": "Sol sablonneux", "options": [0, 1]}),
    ("Soil_Type_Silt", st.selectbox, {"label": "Sol limoneux", "options": [0, 1]}),
    ("Crop_Barley", st.selectbox, {"label": "Orge", "options": [0, 1]}),
    ("Crop_Cotton", st.selectbox, {"label": "Coton", "options": [0, 1]}),
    ("Crop_Maize", st.selectbox, {"label": "Maïs", "options": [0, 1]}),
    ("Crop_Rice", st.selectbox, {"label": "Riz", "options": [0, 1]}),
    ("Crop_Soybean", st.selectbox, {"label": "Soja", "options": [0, 1]}),
    ("Crop_Wheat", st.selectbox, {"label": "Blé", "options": [0, 1]}),
    ("Weather_Condition_Cloudy", st.selectbox, {"label": "Temps nuageux", "options": [0, 1]}),
    ("Weather_Condition_Rainy", st.selectbox, {"label": "Temps pluvieux", "options": [0, 1]}),
    ("Weather_Condition_Sunny", st.selectbox, {"label": "Temps ensoleillé", "options": [0, 1]}),
]

exclude = []
if pred_yield:
    exclude.append("Yield_tons_per_hectare")
if pred_irrig:
    exclude.append("Irrigation_Used")
if pred_fert:
    exclude.append("Fertilizer_Used")

user_inputs = {}
cols = st.columns(3)
for idx, (name, func, params) in enumerate(fields):
    if name in exclude:
        user_inputs[name] = 0.0 if func == st.number_input else 0
    else:
        with cols[idx % 3]:
            user_inputs[name] = func(**params)

if st.button("Prédire"):
    data = user_inputs.copy()
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
                st.success(f"🌱 Rendement prédit : {result['yield_prediction']} t/ha")
            if pred_irrig and "irrigation_prediction" in result:
                st.info(f"💧 Irrigation nécessaire : {'Oui' if result['irrigation_prediction'] else 'Non'}")
            if pred_fert and "fertilizer_prediction" in result:
                st.info(f"🧪 Fertilisation nécessaire : {'Oui' if result['fertilizer_prediction'] else 'Non'}")
            if not (pred_yield or pred_irrig or pred_fert):
                st.warning("⚠️ Coche au moins une case pour prédire.")
        else:
            st.error("❌ Erreur lors de la prédiction.")
    except Exception as e:
        st.error(f"❌ Erreur lors de la connexion à l'API : {e}")

st.markdown("---")
st.caption("Projet MLOps - Franès ADONON")