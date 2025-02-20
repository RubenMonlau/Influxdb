import asyncio
import websockets

async def receive_data():
    uri = "ws://172.17.0.2:8765"  # Ajusta la IP según tu servidor WebSocket
    light_on = False  # Estado de la luz
    pump_on = False   # Estado de la bomba de agua

    async with websockets.connect(uri) as websocket:
        print("Conectado al servidor WebSocket")
        try:
            while True:
                message = await websocket.recv()
                print(f"Datos recibidos: {message}")

                try:
                    # Procesar datos de luz
                    if "Luz" in message:
                        light_level = float(message.split("Luz: ")[1].split("lx")[0])
                        
                        # Actuación: encender o apagar la luz
                        if light_level < 200 and not light_on:
                            print("🌑 Está oscuro! Encendiendo luz...")
                            await websocket.send("ACTUATOR: LIGHT ON")
                            light_on = True
                        elif light_level >= 250 and light_on:
                            print("☀️ Hay suficiente luz! Apagando luz...")
                            await websocket.send("ACTUATOR: LIGHT OFF")
                            light_on = False

                        # Alertas para condiciones críticas de luz
                        if light_level < 100:
                            print("🚨 ALERTA: Nivel de luz críticamente bajo!")
                            await websocket.send("ALERT: LIGHT CRITICAL LOW")
                        elif light_level > 1200:
                            print("🚨 ALERTA: Nivel de luz críticamente alto!")
                            await websocket.send("ALERT: LIGHT CRITICAL HIGH")
                    
                    # Procesar datos de humedad
                    if "Humedad" in message:
                        humidity = float(message.split("Humedad: ")[1].split("%")[0])
                        
                        # Actuación: activar o desactivar la bomba de agua
                        if humidity < 40 and not pump_on:
                            print("💦 Suelo seco! Activando bomba de agua...")
                            await websocket.send("ACTUATOR: PUMP ON")
                            pump_on = True
                        elif humidity > 50 and pump_on:
                            print("✅ Humedad suficiente! Apagando bomba...")
                            await websocket.send("ACTUATOR: PUMP OFF")
                            pump_on = False

                        # Alertas para condiciones críticas de humedad
                        if humidity < 30:
                            print("🚨 ALERTA: Humedad críticamente baja!")
                            await websocket.send("ALERT: HUMIDITY CRITICAL LOW")
                        elif humidity > 70:
                            print("🚨 ALERTA: Humedad críticamente alta!")
                            await websocket.send("ALERT: HUMIDITY CRITICAL HIGH")
                
                except ValueError:
                    print("Error al procesar los datos.")

        except websockets.exceptions.ConnectionClosed:
            print("Conexión cerrada por el servidor.")

if __name__ == "__main__":
    asyncio.run(receive_data())
