import pandas as pd
import numpy as np
from scipy import stats
from warnings import simplefilter



class Calculator:

    def __init__(self, archivo):
        self.archivo = archivo


    simplefilter(action='ignore', category=FutureWarning)
        
    def fileSelect(self):
        return self.archivo #data = pd.read_csv(self.archivo, delimiter=" ", header=None)

    
    
    def calculateMean(self, data):
        mean = float(0)
        mean = np.mean(data)
        return mean

    def calculateMedian(self, data):
        median = 0
        median = np.median(data)
        return median

    def calculateMode(self,data):
        mode_res = 0
        mode_res = stats.mode(data, axis=None)
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

    def performCalculations(self):
        data = self.fileSelect()
        data = pd.read_csv(data, delimiter=" ", header=None)

        print(f'Media: {self.calculateMean(data)}')
        print(f'Mediana: {self.calculateMedian(data)}')
        print(f'Moda: {self.calculateMode(data)}')

        print(f'Varianza: {self.calculateVariance(data)}')
        print(f'Desviación Media: {self.calculateMeanDeviation(self.calculateMean(data))}')
        print(f'Desviación Estándar: {self.calculateStandardDeviation(data)}')

