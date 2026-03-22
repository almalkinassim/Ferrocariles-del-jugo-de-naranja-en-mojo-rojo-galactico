import random as rd
import json 
import Planete

with open("nombres.json","r") as nom:
    listNmbr = json.load(nom)


class Galaxia: #GENERA LOS PLANETAS UNICAMENTE 
    def __init__(self):
        self.listPlnt: list[Planete.Planete] = []
        self.NovoPlanete : Planete.Planete # hay que definir esto como un atributop como Planeta 
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
                self.NovoPlanete = Planete.Planete(self.nombreCoplt, self.coordx, self.coordy)
            else:
                self.coordx += 16 
                self.coordy += 16# asi deberia de evitar ya que registra esta nueva variable y luego la anota en las listas es decir que estas coords +16 ya no se usarian
                self.NovoPlanete = Planete.Planete(self.nombreCoplt, self.coordx, self.coordy)
            self.listPlnt.append(self.NovoPlanete)
            

            #Python funciona leyendo linea por line es decir PRIMERO verficamos que las coordenadas no estan en la lista y LUEGOQ se pone en la lista
            ListCoordx.append(self.coordx)
            ListCoordy.append(self.coordy)
        #para evitar que se duplique el sprite; mejor cambiar a % para distancia y camino
        #self.listPlnt.append(self.listPlnt[0]) 
        return self.listPlnt 
    
    