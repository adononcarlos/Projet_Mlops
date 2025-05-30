import requests

def test_predict_all():
    url = "http://127.0.0.1:8000/predict/"
    data = {
        "Rainfall_mm": 500.0,
        "Temperature_Celsius": 25.0,
        "Fertilizer_Used": 1,
        "Irrigation_Used": 0,
        "Days_to_Harvest": 100,
        "Yield_tons_per_hectare": 4.5,
        "Region_East": 1,
        "Region_North": 0,
        "Region_South": 0,
        "Region_West": 0,
        "Soil_Type_Chalky": 0,
        "Soil_Type_Clay": 1,
        "Soil_Type_Loam": 0,
        "Soil_Type_Peaty": 0,
        "Soil_Type_Sandy": 0,
        "Soil_Type_Silt": 1,
        "Crop_Barley": 0,
        "Crop_Cotton": 0,
        "Crop_Maize": 1,
        "Crop_Rice": 0,
        "Crop_Soybean": 0,
        "Crop_Wheat": 0,
        "Weather_Condition_Cloudy": 1,
        "Weather_Condition_Rainy": 0,
        "Weather_Condition_Sunny": 0
    }
    params = {
        "predict_yield": True,
        "predict_irrig": True,
        "predict_fert": True
    }
    response = requests.post(url, params=params, json=data)
    assert response.status_code == 200
    result = response.json()
    assert "yield_prediction" in result
    assert "irrigation_prediction" in result
    assert "fertilizer_prediction" in result