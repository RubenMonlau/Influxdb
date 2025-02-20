import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from connection_component import InfluxDBConnection

# --- Functions to get sensor data from InfluxDB ---

def get_light_data():
    """Recupera los datos del sensor de luz de los últimos 10 minutos."""
    connection = InfluxDBConnection(
        url="http://172.17.0.2:8086",
        token="J_BBTcBVzZGhw9t7eCpDB8qLR8Md_ZDmor1MAwYsFLIYhi6wo6e41QWF1zjQzRFesV2HNESYowUOW9GckJcxDg==",
        org="rubenrod",
        bucket="rubenrod"
    )
    client = connection.get_client()
    query_api = connection.get_query_api(client)
    
    query = f'''
    from(bucket: "{connection.bucket}")
        |> range(start: -10m)
        |> filter(fn: (r) => r._measurement == "light_sensor" and r._field == "light")
        |> yield(name: "light_data")
    '''
    tables = query_api.query_data_frame(query)
    if tables.empty:
        return pd.DataFrame()
    
    df = tables[['_time', '_value']].rename(columns={"_time": "Time", "_value": "Luz"})
    df['Time'] = pd.to_datetime(df['Time'])
    df.set_index('Time', inplace=True)
    return df

def get_humidity_data():
    """Recupera los datos del sensor de humedad de los últimos 10 minutos."""
    connection = InfluxDBConnection(
        url="http://172.17.0.2:8086",
        token="J_BBTcBVzZGhw9t7eCpDB8qLR8Md_ZDmor1MAwYsFLIYhi6wo6e41QWF1zjQzRFesV2HNESYowUOW9GckJcxDg==",
        org="rubenrod",
        bucket="rubenrod"
    )
    client = connection.get_client()
    query_api = connection.get_query_api(client)
    
    query = f'''
    from(bucket: "{connection.bucket}")
        |> range(start: -10m)
        |> filter(fn: (r) => r._measurement == "humidity_sensor" and r._field == "humidity")
        |> yield(name: "humidity_data")
    '''
    tables = query_api.query_data_frame(query)
    if tables.empty:
        return pd.DataFrame()
    
    df = tables[['_time', '_value']].rename(columns={"_time": "Time", "_value": "Humedad"})
    df['Time'] = pd.to_datetime(df['Time'])
    df.set_index('Time', inplace=True)
    return df

def get_co2_data():
    """Recupera los datos del sensor de CO₂ de los últimos 10 minutos."""
    connection = InfluxDBConnection(
        url="http://172.17.0.2:8086",
        token="J_BBTcBVzZGhw9t7eCpDB8qLR8Md_ZDmor1MAwYsFLIYhi6wo6e41QWF1zjQzRFesV2HNESYowUOW9GckJcxDg==",
        org="rubenrod",
        bucket="rubenrod"
    )
    client = connection.get_client()
    query_api = connection.get_query_api(client)
    
    query = f'''
    from(bucket: "{connection.bucket}")
        |> range(start: -10m)
        |> filter(fn: (r) => r._measurement == "co2_sensor" and r._field == "co2")
        |> yield(name: "co2_data")
    '''
    tables = query_api.query_data_frame(query)
    if tables.empty:
        return pd.DataFrame()
    
    df = tables[['_time', '_value']].rename(columns={"_time": "Time", "_value": "CO₂"})
    df['Time'] = pd.to_datetime(df['Time'])
    df.set_index('Time', inplace=True)
    return df

# --- Update function for the animation ---

def update(frame):
    """Actualiza las gráficas en tiempo real para cada sensor."""
    global ax1, ax2, ax3

    # Recuperar datos de cada sensor
    df_light = get_light_data()
    df_humidity = get_humidity_data()
    df_co2 = get_co2_data()

    # Actualizar gráfica del sensor de luz
    ax1.clear()
    if not df_light.empty:
        ax1.plot(df_light.index, df_light['Luz'], marker='o', linestyle='-', color='orange')
    ax1.set_title("Sensor de Luz - Últimos 10 minutos")
    ax1.set_xlabel("Tiempo")
    ax1.set_ylabel("Luz (lx)")
    ax1.grid(True)

    # Actualizar gráfica del sensor de humedad
    ax2.clear()
    if not df_humidity.empty:
        ax2.plot(df_humidity.index, df_humidity['Humedad'], marker='o', linestyle='-', color='blue')
    ax2.set_title("Sensor de Humedad - Últimos 10 minutos")
    ax2.set_xlabel("Tiempo")
    ax2.set_ylabel("Humedad (%)")
    ax2.grid(True)

    # Actualizar gráfica del sensor de CO₂
    ax3.clear()
    if not df_co2.empty:
        ax3.plot(df_co2.index, df_co2['CO₂'], marker='o', linestyle='-', color='green')
    ax3.set_title("Sensor de CO₂ - Últimos 10 minutos")
    ax3.set_xlabel("Tiempo")
    ax3.set_ylabel("CO₂ (ppm)")
    ax3.grid(True)

# --- Function to create and show the real-time plots ---

def plot_realtime_sensors():
    """Crea una gráfica con 3 subplots para Luz, Humedad y CO₂ en tiempo real."""
    global ax1, ax2, ax3

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    ani = FuncAnimation(fig, update, interval=5000)  # Actualiza cada 5 segundos
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_realtime_sensors()