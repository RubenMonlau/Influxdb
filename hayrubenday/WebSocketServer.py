import asyncio
import websockets
import pandas as pd
from connection_component import InfluxDBConnection
import warnings
from influxdb_client.client.warnings import MissingPivotFunction

warnings.simplefilter("ignore", MissingPivotFunction)

async def send_sensor_data(websocket, path):
    """Envía datos en tiempo real de los sensores (luz y humedad) a los clientes conectados."""
    connection = InfluxDBConnection(
        url="http://localhost:8086",
        token="J_BBTcBVzZGhw9t7eCpDB8qLR8Md_ZDmor1MAwYsFLIYhi6wo6e41QWF1zjQzRFesV2HNESYowUOW9GckJcxDg==",
        org="rubenrod",
        bucket="rubenrod"
    )

    client = connection.get_client()
    query_api = connection.get_query_api(client)

    last_timestamp_light = None
    last_timestamp_humidity = None

    try:
        while True:
            # Consulta los últimos datos de luz
            query_light = f'''
            from(bucket: "{connection.bucket}")
                |> range(start: -10s)
                |> filter(fn: (r) => r._measurement == "light_sensor" and r._field == "light")
            '''
            tables_light = query_api.query_data_frame(query_light)
            if not tables_light.empty:
                df_light = tables_light[['_time', '_value']].rename(columns={"_time": "Time", "_value": "Luz"})
                df_light['Time'] = pd.to_datetime(df_light['Time'])
                new_light = df_light[df_light['Time'] > (last_timestamp_light or df_light['Time'].min())]
                if not new_light.empty:
                    last_timestamp_light = new_light['Time'].max()
                    for _, row in new_light.iterrows():
                        await websocket.send(f"Tiempo: {row['Time']}, Luz: {row['Luz']} lx")

            # Consulta los últimos datos de humedad
            query_humidity = f'''
            from(bucket: "{connection.bucket}")
                |> range(start: -10s)
                |> filter(fn: (r) => r._measurement == "humidity_sensor" and r._field == "humidity")
            '''
            tables_humidity = query_api.query_data_frame(query_humidity)
            if not tables_humidity.empty:
                df_humidity = tables_humidity[['_time', '_value']].rename(columns={"_time": "Time", "_value": "Humedad"})
                df_humidity['Time'] = pd.to_datetime(df_humidity['Time'])
                new_humidity = df_humidity[df_humidity['Time'] > (last_timestamp_humidity or df_humidity['Time'].min())]
                if not new_humidity.empty:
                    last_timestamp_humidity = new_humidity['Time'].max()
                    for _, row in new_humidity.iterrows():
                        await websocket.send(f"Tiempo: {row['Time']}, Humedad: {row['Humedad']}%")

            await asyncio.sleep(5)  # Espera 5 segundos entre consultas
    except websockets.exceptions.ConnectionClosed:
        print("Conexión cerrada con el cliente.")

# Inicia el servidor WebSocket
async def main():
    server = await websockets.serve(send_sensor_data, "0.0.0.0", 8765)
    print("Servidor WebSocket iniciado en ws://0.0.0.0:8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
