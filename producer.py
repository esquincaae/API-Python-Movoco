import serial
import statistics
import json
import time
from rabbitmq import RabbitMQ
from warnings import simplefilter

# Configuración del puerto serie (serial)
port = "COM6"  # Cambia esto al puerto correcto donde está conectado tu Arduino
baudrate = 9600

# Configuración de RabbitMQ
rabbitmq_host = "18.210.152.12"
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
simplefilter(action='ignore', category=FutureWarning)
ser = serial.Serial(port, baudrate)

# Listas para almacenar los datos de los sensores

amp_data = []
volt_data = []# Lista para almacenar los datos del valor de amp

# Bucle principal
while True:
    # Lectura de datos desde el puerto serie (serial)
    line = ser.readline().decode().strip()
    print(line)
    data = []
    data = line.split(",")
    amp_data.append(float(data[0]))
    volt_data.append(float(data[1]))

    if len(volt_data) > 1:
        # Cálculo de la media, desviación estándar, desviación media y varianza
        volt_mean = statistics.mean(volt_data)
        volt_stdev = statistics.stdev(volt_data)
        volt_mean_dev = statistics.mean([abs(x - volt_mean) for x in volt_data])
        volt_variance = statistics.variance(volt_data)

        volt_data_dict = {
            "volt": volt_data[-1],
            "media": volt_mean,
            "variance": volt_variance,
            "standardDeviation": volt_stdev,
            "meanDeviation": volt_mean_dev,
            "user_id":1
        }

        # Convertir el diccionario a JSON
        volt_json_data = json.dumps(volt_data_dict)

        # Envío de los datos de la tasa de flujo de agua a RabbitMQ
        rabbit.send(rabbitmq_exchange, "voltSensorData", volt_json_data)

    # Realizar operaciones con los datos de amp
    if len(amp_data) > 1:
        # Cálculo de la media, desviación estándar, desviación media y varianza del 
        amp_mean = statistics.mean(amp_data)
        amp_stdev = statistics.stdev(amp_data)
        amp_mean_dev = statistics.mean([abs(x - amp_mean) for x in amp_data])
        amp_variance = statistics.variance(amp_data)

        amp_data_dict = {
            "amp": amp_data[-1],
            "media": amp_mean,
            "variance": amp_variance,
            "standardDeviation": amp_stdev,
            "meanDeviation": amp_mean_dev,
            "user_id":1
        }

        # Convertir el diccionario a JSON
        amp_json_data = json.dumps(amp_data_dict)

        # Envío de los datos del amp a RabbitMQ
        rabbit.send(rabbitmq_exchange, "ampSensorData", amp_json_data)
        # print("Datos de amp enviados correctamente a RabbitMQ.")

    
        
    
# Cierre de conexiones
ser.close()
