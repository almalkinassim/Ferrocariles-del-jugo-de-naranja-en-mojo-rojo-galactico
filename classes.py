import random as rd
import math
import copy as cp
import json


with open("nombres.json","r") as nom:
    listNmbr = json.load(nom)


# On definit le planète par son nom (composé de 2 noms), et ses coordonées
class Planete:
    def __init__(self,NomP: str, x: int, y: int): #__init__ sert à initialiser la classe pour pouvoir assigner les valeurs
        self.NomP = NomP
        self.x = x
        self.y = y
       
   
    def __repr__(self):
        #Sans ça c'est mort ça donne des caractèeres sombres et obscures
        # ! que hace repr? Es como ToString en Java
        return f"[{self.NomP} | Coordonnées: ({self.x}, {self.y})]"
       
class Galaxie: #GENERA LOS PLANETAS UNICAMENTE


    def __init__(self):
        self.listPlnt: list[Planete] = []
        self.NovoPlanete : Planete # hay que definir esto como un atributop como Planeta
        self.nombreCoplt : str
        self.coordx : int
        self.coordy : int


    def SamsungGalaxy(self,n: int):
        ListCoordx = []
        ListCoordy = []
        for i in range(n):
            #GENERACION ALEATORIA DE LOS NOMBRES
            nombre1 = rd.choice(listNmbr)
            nombre2 = rd.choice(listNmbr)
            n1 = nombre1["nom1"]
            n2 = nombre2["nom2"]
            self.nombreCoplt = f"{n1} {n2}"
           
            #GENERACION ALEATORIA DE LAS COORDENADAS
            rdint = rd.randint
            self.coordx = rdint(1,28)*32 # la taille de la ventana y 32 porque los planetas son de 32 pixels
            self.coordy = rdint(1,21)*32
           
            if(self.coordx not in ListCoordx and self.coordy not in ListCoordy):# para evitar super posiciones
                self.NovoPlanete = Planete(self.nombreCoplt, self.coordx, self.coordy)
            else:
                self.NovoPlanete = Planete(self.nombreCoplt, self.coordx+16, self.coordy+16)
            self.listPlnt.append(self.NovoPlanete)
           
            # ! podemos volver a usar while, si le damos un numero maximo de intentos para evitar un bucle inf, por ahora seguir usando elif


            #while(self.coordx in ListCoordx and   self.coordy in ListCoordy):# tiene que ser un while
            #    self.coordx = rdint(1,28)*32 # mientras las coordenadas esten en la lista entoces dame otras
            #    self.coordy = rdint(1,21)*32
            #self.NovoPlanete = Planete(self.nombreCoplt, self.coordx, self.coordy)
            #self.listPlnt.append(self.NovoPlanete)
               
            #Python funciona leyendo linea por line es decir PRIMERO verficamos que las coordenadas no estan en la lista y LUEGOQ se pone en la lista
            ListCoordx.append(self.coordx)
            ListCoordy.append(self.coordy)
        #para evitar que se duplique el sprite; mejor cambiar a % para distancia y camino
        #self.listPlnt.append(self.listPlnt[0])
        return self.listPlnt
   
   
#MEZCLA LA GALAXIA PARA OBTENER M ITINERARIOS DIFERENTES
class Itineraires():


    def __init__(self, Galx : Galaxie):
        self.Galx = Galx
        self.distTot = 0
        self.itinerarios = []


   #generation aleatoire de m itineraires
    def genererRd(self, m: int):
        self.itinerarios = [] # evite duplicats avec boucle de simulations
        plnt_init = self.Galx.listPlnt[0]
        for i in range(m):
            chemin = self.Galx.listPlnt[1:]
            rd.shuffle(chemin)
            self.itinerarios.append([plnt_init] + chemin)


    def Dist(self, chemin):
        self.distTot = 0 # eviter accumulation..
        if(len(chemin)>0):#el primer index es 0 asi que  decimos que calcule las distancias solo cuando haya mas de 1 planeta
            for i in range(len(chemin)):# va parcorrir toute la liste et prend le x et y du premier planete et du suivant
                p1 = chemin[i]#guarda el primero
                p2 = chemin[(i + 1) % len(chemin)] #permet de creer un circuit fermé
                dist = math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2) # formula de la distancia entre dos puntos en un plano cartesiano
                self.distTot += dist
            return self.distTot


    def mutation(self, p: float):
        for chemin in self.itinerarios:
            if rd.randint(1, 100) <= p * 100: # si el numero aleatorio es menor que la probabilidad de mutacion entonces se muta el itinerario
                #indices commencent a 1 pour eviter de melanger le premier planete
                i = rd.randint(1, len(chemin) - 1)
                j = rd.randint(1, len(chemin) - 1)
                chemin[i], chemin[j] = chemin[j], chemin[i] # intercambia los planetas en esos idx


    def croisement(self, parent1, parent2):
        size = len(parent1)
   
    # corte
        start = rd.randint(1, size - 4)
        end = start + rd.randint(2, 3)  # longueur 3 ou 4
        segment = parent1[start:end]
        enfant = [parent1[0]]
        enfant += segment
       
    # rellenar con segundo
        for p in parent2:
            if p not in enfant:
                enfant.append(p)
   
        return enfant  




class Tournoi:
    def __init__(self):
        self.chemin = []
        self.FitnessList = []
        self.distance = 0


   
    #Calcula la fitness
    def fitness(self, itin : Itineraires):
        for chemin in itin.itinerarios:
            d = itin.Dist(chemin)
            if d > 0:
                fitness_val = 1 / d
            else:
                fitness_val = float('inf')
            self.FitnessList.append((chemin,fitness_val, d))
        return self.FitnessList
   
    def tournoi(self, rounds: int):
        scores = [0] * len(self.FitnessList) # inicializa los puntajes de cada itinerario a 0
        for i in range(rounds):  
            idx = rd.sample(range(len(self.FitnessList)), 5)
    # escoge al mejor
            best = idx[0]
            for i in idx:
                if self.FitnessList[i][1] > self.FitnessList[best][1]:
                    best = i
    # suma un punto al vencedor
            scores[best] += 1
        return scores


