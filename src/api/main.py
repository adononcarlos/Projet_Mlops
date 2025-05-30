from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# Charger les modèles
model_yield = joblib.load('src/models/random_forest_model.pkl')
model_irrig = joblib.load('src/models/random_forest_irrigation.pkl')
model_fert = joblib.load('src/models/random_forest_fertilizer.pkl')

# Définir le schéma d'entrée avec toutes les colonnes sauf la cible de rendement
class InputData(BaseModel):
    Rainfall_mm: float
    Temperature_Celsius: float
    Fertilizer_Used: int
    Irrigation_Used: int
    Days_to_Harvest: int
    Yield_tons_per_hectare: float  # <-- AJOUTE CETTE LIGNE
    Region_East: int
    Region_North: int
    Region_South: int
    Region_West: int
    Soil_Type_Chalky: int
    Soil_Type_Clay: int
    Soil_Type_Loam: int
    Soil_Type_Peaty: int
    Soil_Type_Sandy: int
    Soil_Type_Silt: int
    Crop_Barley: int
    Crop_Cotton: int
    Crop_Maize: int
    Crop_Rice: int
    Crop_Soybean: int
    Crop_Wheat: int
    Weather_Condition_Cloudy: int
    Weather_Condition_Rainy: int
    Weather_Condition_Sunny: int

@app.post("/predict/")
def predict(
    data: InputData,
    predict_yield: bool = True,
    predict_irrig: bool = True,
    predict_fert: bool = True
):
    input_dict = data.dict()
    results = {}

    # Pour chaque prédiction, on retire la colonne cible de l'input
    if predict_yield:
        X = pd.DataFrame([{
            k: v for k, v in input_dict.items() if k != "Yield_tons_per_hectare"
        }])
        results["yield_prediction"] = model_yield.predict(X)[0]
    if predict_irrig:
        X = pd.DataFrame([{
            k: v for k, v in input_dict.items() if k != "Irrigation_Used"
        }])
        results["irrigation_prediction"] = int(model_irrig.predict(X)[0])
    if predict_fert:
        X = pd.DataFrame([{
            k: v for k, v in input_dict.items() if k != "Fertilizer_Used"
        }])
        results["fertilizer_prediction"] = int(model_fert.predict(X)[0])

    return results