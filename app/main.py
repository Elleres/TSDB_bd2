from typing import Optional

from fastapi import FastAPI
from app.services.sensor_service import inserir_sensor, consultar_sensores

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API FastAPI + InfluxDB funcionando!"}

@app.post("/insert/")
def insert_sensor(localizacao: str, temperatura: float, umidade: float, vento: float):
    return inserir_sensor(localizacao, temperatura, umidade, vento)

@app.get("/consulta/")
def get_sensores(query: Optional[str] = None):
    return consultar_sensores(query)