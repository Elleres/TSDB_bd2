import os

from influxdb_client import InfluxDBClient, WriteApi, QueryApi


class InfluxDBConnection:
    """Classe para gerenciar a conexão com o TSDB"""
    def __init__(self):
        self.url = "http://influxdb:8086"
        self.token = "meutoken"
        self.org =  "meuorg"
        self.bucket = "meubucket"

        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.write_api: WriteApi = self.client.write_api()
        self.query_api: QueryApi = self.client.query_api()

    def write(self, point):
        """Escrever um ponto no bd"""
        self.write_api.write(bucket=self.bucket,org=self.org ,record=point)

    def query(self, query):
        """Executa uma query no bd"""
        return self.query_api.query(org=self.org, query=query)

    def close(self):
        """Fecha a conexão com o banco"""
        self.client.close()

influx_db = InfluxDBConnection()