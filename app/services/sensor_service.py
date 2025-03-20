from datetime import datetime
from typing import Optional

from influxdb_client import Point
from app.db.config import influx_db


def inserir_sensor(localizacao: str, temperatura: float, umidade: float, vento: float):
    """
    Insere dados de um sensor no InfluxDB.
    """

    point = Point("sensores").tag("localizacao", localizacao)

    point = point.field("temperatura", temperatura)

    point = point.field("umidade", umidade)

    point = point.field("vento", vento)

    influx_db.write(point)
    return {"message": "Dado inserido com sucesso"}


def consultar_sensores(query: Optional[str]):
    """
    Retorna os últimos dados de sensores armazenados no InfluxDB.
    """
    if not query:
        query = f'''
        from(bucket: "{influx_db.bucket}")
          |> range(start: -10m)
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