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
            # Generate a random light value between 100 and 1000 lux.
            luz = round(random.uniform(100, 1000), 2)
            point_light = Point("light_sensor").field("light", luz)
            write_api.write(bucket=connection.bucket, org=connection.org, record=point_light)
            print(f"Luz enviada: {luz} lx")
            time.sleep(5)  # Simula el envío cada 5 segundos
    except KeyboardInterrupt:
        print("Simulación detenida.")

if __name__ == "__main__":
    simulate_temperature_data()
