import serial
import statistics
import json
import time
from rabbitmq import RabbitMQ

# Configuración del puerto serie (serial)
port = "COM6"  # Cambia esto al puerto correcto donde está conectado tu Arduino
baudrate = 9600

# Configuración de RabbitMQ
rabbitmq_host = "localhost"
rabbitmq_user = "syncronix"
rabbitmq_password = "movoco21720"
rabbitmq_queue_ampSensor = "ampSensor"
rabbitmq_queue_voltSensor = "voltSensor"
rabbitmq_exchange = "movocoName"

rabbit = RabbitMQ(rabbitmq_host, rabbitmq_user, rabbitmq_password)
rabbit.create_exchange("movocoName", "topic")
rabbit.create_queue(rabbitmq_queue_ampSensor)
rabbit.bind_queue(rabbitmq_exchange, rabbitmq_queue_ampSensor, "ampSensorData")
rabbit.create_queue(rabbitmq_queue_voltSensor)
rabbit.bind_queue(rabbitmq_exchange, rabbitmq_queue_voltSensor, "voltSensorData")


# Conexión al puerto serie (serial)
ser = serial.Serial(port, baudrate)

# Listas para almacenar los datos de los sensores

amp_data = []
volt_data = []# Lista para almacenar los datos del valor de amp

# Bucle principal
while True:
    # Lectura de datos desde el puerto serie (serial)
    line = ser.readline().decode().strip()
    print(line)

    if line.startswith("voltSensorData:"):
        value = line[10:]
        volt_data.append(float(value))
    elif line.startswith("ampSensorData:"):
        value = line[3:]
        amp_data.append(float(value))

    if len(volt_data) > 1:
        # Cálculo de la media, desviación estándar, desviación media y varianza
        volt_mean = statistics.mean(volt_data)
        volt_stdev = statistics.stdev(volt_data)
        volt_mean_dev = statistics.mean([abs(x - volt_mean) for x in volt_data])
        volt_variance = statistics.variance(volt_data)

        # print("Tasa de flujo de agua (media):", volt_mean)
        # print("Tasa de flujo de agua (desviación estándar):", volt_stdev)
        # print("Tasa de flujo de agua (desviación media):", volt_mean_dev)
        # print("Tasa de flujo de agua (varianza):", volt_variance)
        # print(
            # "Dato bruto de la tasa de flujo de agua:", data[-1]
        # )  # Último dato almacenado

        # Creación del diccionario con los datos de la tasa de flujo de agua
        volt_data_dict = {
            "volt": volt_data[-1],
            "media": volt_mean,
            "variance": volt_variance,
            "standardDeviation": volt_stdev,
            "meanDeviation": volt_mean_dev,
        }

        # Convertir el diccionario a JSON
        volt_json_data = json.dumps(volt_data_dict)

        # Envío de los datos de la tasa de flujo de agua a RabbitMQ
        rabbit.send(rabbitmq_exchange, "voltSensorData", volt_json_data)
        # print("volt")
        # print(volt_json_data)
        # print("Datos de tasa de flujo de agua enviados correctamente a RabbitMQ.")

    # Realizar operaciones con los datos de amp
    if len(amp_data) > 1:
        # Cálculo de la media, desviación estándar, desviación media y varianza del 
        amp_mean = statistics.mean(amp_data)
        amp_stdev = statistics.stdev(amp_data)
        amp_mean_dev = statistics.mean([abs(x - amp_mean) for x in amp_data])
        amp_variance = statistics.variance(amp_data)

        # print("Valor de amp (media):", amp_mean)
        # print("Valor de amp (desviación estándar):", amp_stdev)
        # print("Valor de amp (desviación media):", amp_mean_dev)
        # print("Valor de amp (varianza):", amp_variance)
        # print("Dato bruto de amp:", amp_data[-1])  # Último dato almacenado

        # Creación del diccionario con los datos del amp
        amp_data_dict = {
            "amp": amp_data[-1],
            "media": amp_mean,
            "variance": amp_variance,
            "standardDeviation": amp_stdev,
            "meanDeviation": amp_mean_dev
        }

        # Convertir el diccionario a JSON
        amp_json_data = json.dumps(amp_data_dict)

        # Envío de los datos del amp a RabbitMQ
        rabbit.send(rabbitmq_exchange, "ampSensorData", amp_json_data)
        print("amp")
        # print("Datos de amp enviados correctamente a RabbitMQ.")

    
        
    
# Cierre de conexiones
ser.close()