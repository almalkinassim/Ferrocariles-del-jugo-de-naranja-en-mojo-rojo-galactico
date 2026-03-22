import random as rd
import math
import matplotlib as mat

import Planete
import Galaxia 
import Itinerarios as IT
import main

Galx = Galaxia.Galaxia()
Itin = IT.Itinerarios(Galx)

class Torneo:
    def __init__(self):
        self.fitness = 0
        self.chemin = []
        self.FitnessList = []
        self.distance = 0

#Calcula la fitness
    def CalculoFit(self):
        for chemin in Itin.itinerarios:
            d = Itin.Dist(chemin)
            if d != 0:
                self.fitness = 1 / d
            else:
                self.fitness = float('inf')
            self.FitnessList.append((chemin,self.fitness, self.distance))
        #Lo printea
        for chemin, fitness, self.distance in self.FitnessList:
            print("Chemin :", chemin)
            print("Fitness :", fitness)
            print("Distance :", self.distance)
            print("--------------")
        
        
        
        