import serial
import time
from Statistic import Calculator
import pandas
import numpy as np

fileAmp = 'dataAmps.csv'
fileVolt = 'dataVolts.csv'

#instancias de la clase con los metodos estadisticos
calcVolts = Calculator(fileVolt)
calcAmps = Calculator(fileAmp)

serialPort = serial.Serial("COM6", 9600)
time.sleep(1)

amps = []
volts = []

while True:
    decodeSerial = serialPort.readline().decode('ascii')
    print("********")
    
    #separar array
    separateArray = decodeSerial.split(',')

    #cada dato se convierte en una variable distinta
    amper = amper = float(separateArray[0])
    voltage = voltage = float(separateArray[1])

    #se crean arrays de cada dato y se agregan los datos nuevos en loop
    amps.append(amper)
    volts.append(voltage)

    print(amps)
    print(volts)
    #se converten los array a arrays de NumPy
    newAmps = np.array(amps)
    newVolts = np.array(volts)
    #se crean los dataframes
    dfa = pandas.DataFrame(newAmps)
    dfv = pandas.DataFrame(newVolts)

    #se mandan los dataframes a los archivos
    dfa.to_csv('./arduino/dataAmps.csv', sep=" ", index=False)
    dfv.to_csv('./arduino/dataVolts.csv', sep=" ", index=False)

    #fileAmp = 'dataAmps.csv'
    #fileVolt = 'dataVolts.csv'
    #calcAmps.fileSelect(fileAmp)
    #calcVolts.fileSelect(fileVolt)
    print('*******')
    calcAmps.performCalculations()
    print('******')
    calcVolts.performCalculations()
