from influxdb_client import InfluxDBClient

class InfluxDBConnection:
    def __init__(self, url, token, org, bucket):
        self.url = url
        self.token = token
        self.org = org
        self.bucket = bucket

    def get_client(self):
        """Devuelve una instancia del cliente de InfluxDB."""
        return InfluxDBClient(url=self.url, token=self.token, org=self.org)

    def get_write_api(self, client):
        """Devuelve la API de escritura."""
        return client.write_api()

    def get_query_api(self, client):
        """Devuelve la API de consultas."""
        return client.query_api()

# Configuración de conexión
url="http://172.17.0.2:8086"
token="J_BBTcBVzZGhw9t7eCpDB8qLR8Md_ZDmor1MAwYsFLIYhi6wo6e41QWF1zjQzRFesV2HNESYowUOW9GckJcxDg=="
org="rubenrod"
bucket="rubenrod"

# Ejemplo de uso:
if __name__ == "__main__":
    connection = InfluxDBConnection(url, token, org, bucket)
    client = connection.get_client()
    print("Conexión establecida correctamente con InfluxDB.")
