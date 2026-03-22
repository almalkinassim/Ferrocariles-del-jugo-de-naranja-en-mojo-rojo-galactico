#mira esto de aqui
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
        

#MEZCLA LA GALAXIA PARA OBTENER M ITINERARIOS DIFERENTES
