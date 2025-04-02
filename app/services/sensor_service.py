import random

from datetime import datetime, timedelta, timezone
from typing import Optional

from influxdb_client import Point
from app.db.config import influx_db


def gerar_dados_sensores():
    sensores = ["LabCOMP1", "LabCOMP2", "LabCOMP3"]
    total_leituras = 100

    dados = []

    for sensor in sensores:
        leituras = []

        for _ in range(total_leituras):
            temperatura = round(random.uniform(22.0, 30.0), 1)
            umidade = round(random.uniform(45.0, 70.0), 1)
            vento = round(random.uniform(0.0, 10.0), 1)

            leitura = {
                "temperatura": temperatura,
                "umidade": umidade,
                "vento": vento
            }

            leituras.append(leitura)

        dados.append({
            "localizacao": sensor,
            "leituras": leituras
        })

    return dados

def inserir_sensor(localizacao: str, temperatura: float, umidade: float, vento: float, tempo: Optional[datetime] = datetime.now()):
    """
    Insere dados de um sensor no InfluxDB.
    """

    point = Point("sensores").tag("localizacao", localizacao)

    point = point.field("temperatura", temperatura)

    point = point.field("umidade", umidade)

    point = point.field("vento", vento)

    point = point.time(tempo)
    influx_db.write(point)
    return {"message": "Dado inserido com sucesso"}


def inserir_multiplos_sensores():
    """
    Insere múltiplas leituras de múltiplos sensores no InfluxDB (um ponto por vez).
    """
    dados = gerar_dados_sensores()
    tempo_inicial = datetime.now()
    for sensor in dados:
        i = 0
        localizacao = sensor["localizacao"]
        for leitura in sensor["leituras"]:
            agora = tempo_inicial - timedelta(hours=i)
            inserir_sensor(localizacao, leitura['temperatura'], leitura["umidade"], leitura["vento"], agora)
            i += 1




def consultar_sensores(query: Optional[str]):
    """
    Retorna os últimos dados de sensores armazenados no InfluxDB.
    """
    if not query:
        query = f'''
        from(bucket: "{influx_db.bucket}")
          |> range(start: -30d)
          |> filter(fn: (r) => r._measurement == "sensores")
          |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        '''

    result = influx_db.query(query)

    dados = []
    for table in result:
        for record in table.records:
            dados.append({
                "time": record.get_time().isoformat(),
                "localizacao": record.values.get("localizacao"),
                "temperatura": record.values.get("temperatura"),
                "umidade": record.values.get("umidade"),
                "vento": record.values.get("vento"),
            })

    influx_db.close()
    return {"dados": dados}