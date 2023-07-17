import serial
import time
#from Statistic import Calculator
import pandas
import numpy as np


from scipy import stats
from warnings import simplefilter



class Calculator:

    def __init__(self, archivo):
        self.archivo = archivo

    simplefilter(action='ignore', category=FutureWarning)
        
    def calculateMean(self, data):
        mean = float(0)
        mean = np.mean(data)
        return mean

    def calculateMedian(self, data):
        median = 0
        median = np.median(data)
        return median

    def calculateMode(self, data):
        mode_res = 0
        moda = stats.mode(data)
        mode_res = moda.mode[0]
        return mode_res
    
    # Calculamos las medidas de dispersión
    def calculateMeanDeviation(self, data):
        mean_deviation = np.mean(np.abs(data - self.calculateMean(data)))
        return mean_deviation
    
    def calculateStandardDeviation(self, data):
        variance = np.var(data)
        return variance
    
    def calculateVariance(self, data):
        standard_deviation = np.std(data)
        return standard_deviation

    def performCalculations(self, archivo):
        data = archivo
        data = pandas.read_csv(data, delimiter=" ", header=None)


        print(f'Media: {self.calculateMean(data)}')
        print(f'Mediana: {self.calculateMedian(data)}')
        print(f'Moda: {self.calculateMode(data)}')

        print(f'Varianza: {self.calculateVariance(data)}')
        print(f'Desviación Media: {self.calculateMeanDeviation(data)}')
        print(f'Desviación Estándar: {self.calculateStandardDeviation(data)}')




















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

    #print(amps)
    #print(volts)
    #se converten los array a arrays de NumPy
    newAmps = np.array(amps)
    newVolts = np.array(volts)
    #se crean los dataframes
    dfa = pandas.DataFrame(newAmps)
    dfv = pandas.DataFrame(newVolts)

    #se mandan los dataframes a los archivos
    dfa.to_csv('C:/Users/Esquinca/Desktop/pyserial/arduino/dataAmps.csv', sep=" ", index=False)
    dfv.to_csv('C:/Users/Esquinca/Desktop/pyserial/arduino/dataVolts.csv', sep=" ", index=False)

    fileAmp = 'C:/Users/Esquinca/Desktop/pyserial/arduino/dataAmps.csv'
    fileVolt = 'C:/Users/Esquinca/Desktop/pyserial/arduino/dataVolts.csv'
    #calcAmps.fileSelect(fileAmp)
    #calcVolts.fileSelect(fileVolt)
    print('***AMPS***')
    calcAmps.performCalculations(fileAmp)
    print('***VOLTS***')
    calcVolts.performCalculations(fileVolt)