import random
import time
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from connection_component import InfluxDBConnection

def simulate_temperature_data():
    """Simula el envío de datos de temperatura cada 5 segundos."""
    connection = InfluxDBConnection(
        url="http://172.17.0.2:8086",
        token="J_BBTcBVzZGhw9t7eCpDB8qLR8Md_ZDmor1MAwYsFLIYhi6wo6e41QWF1zjQzRFesV2HNESYowUOW9GckJcxDg==",
        org="rubenrod",
        bucket="rubenrod"
    )
    
    client = connection.get_client()
    write_api = connection.get_write_api(client)

    try:
        while True:
            # Generate a random humidity value between 30 and 90%.
            humedad = round(random.uniform(30, 90), 2)
            point_humidity = Point("humidity_sensor").field("humidity", humedad)
            write_api.write(bucket=connection.bucket, org=connection.org, record=point_humidity)
            print(f"Humedad enviada: {humedad}%")
            time.sleep(5)  # Simula el envío cada 5 segundos
    except KeyboardInterrupt:
        print("Simulación detenida.")

if __name__ == "__main__":
    simulate_temperature_data()
