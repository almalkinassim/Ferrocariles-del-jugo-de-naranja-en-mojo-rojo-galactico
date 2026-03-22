import random as rd
import math
import copy as cp
import main
import Galaxia


class Itinerarios():
    def __init__(self, Galx : Galaxia.Galaxia):
        self.Galx = Galx
        self.distTot = 0
        self.fit = 0
        self.itinerarios = []

    #MODIFS - PARA QUE SEA COMO EL PROBLEMA: EL PRIMER PLANETA ES EL MISMO PARA TODOS LOS ITINERARIOS, ASI QUE NO SE MEZCLA EL PRIMER PLANETA
    #generation aleatoire de m itineraires
    def genererRd(self, m: int):
        for i in range(m):
            shuflPlnt = self.Galx.listPlnt.copy() 
            rd.shuffle(shuflPlnt)
            self.itinerarios.append(shuflPlnt)

    #generation de m itineraires a partir de itinerarios existentes
    def genererHerit(self, m: int, p: int):
        for i in range(m):
            shuflPlnt = self.itinerarios[i]
            self.itinerarios.append(shuflPlnt)

    def Dist(self, chemin):
        #if(len(chemin)>0):#el primer index es 0 asi que  decimos que calcule las distancias solo cuandi haya mas de 1 planeta
            for i in range(len(chemin)-1):# va parcorrir todo la lista y va coger el x y el y del primer planeta y del siguiente
                p1 = chemin[i]#guarda el primero
                p2 = chemin[i + 1]
                dist = math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2) # formula de la distancia entre dos puntos en un plano cartesiano
                self.distTot += dist
            return self.distTot
    
    def fitness(self, it):  
        fitness_list = []
        for i in range(len(it)):
            d = self.Dist(it[i])
            if d != 0:
                fit = 1/d
                fitness_list.append(fit)
            else:
                fitness_list.append(float('inf'))  # max au cas ou distance nulle (1 planete)
        return fitness_list

    def nouvellegen(self, m: int, p: int):
        prevgen = cp.copy(self)
        #modificar para que esten tambien en order creciente
        #creo que no es con prevgen, despues testeo
        # m se puede remplazar por el tamano de la poblacion tambien
        h = 1
        n = 2
        while(h > 0):
            h = round(m/n**2)
            prevgen.genererHerit(h, p)
            n += 1
        #que el resto de los itinerarios sean aleatorios (como los "faibles" del torneo de akshay)
        for i in range(m - h): #no es h, si no un contador de cuanos itinerarios se han generado con la herencia, porque h es el numero de itinerarios generados en la ultima iteracion del while, pero antes se han generado otros h itinerarios, entonces el numero de itinerarios faltan para llegar a m 
            prevgen.genererRd(1) #porque 1?