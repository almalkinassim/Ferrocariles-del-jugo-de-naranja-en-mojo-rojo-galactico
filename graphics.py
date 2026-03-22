import random
import tkinter as tkr
from PIL import Image, ImageTk 


class PlanetSprite:
  #canvas: afficher dans la fenetre, planet: coord, path: trouver l'image 
  def __init__(self,canvas,planet,path): 
    self.canvas = canvas
    self.planet = planet
  

    # detallar como encontrar photo -> PIL.ImageTK no sirvio pero PIL.Image si ;-;
    img = Image.open(path) #charge image 
    imgsz = img.resize((64,64)) 
    self.photo = ImageTk.PhotoImage(imgsz) #la fait lisible pour tkinter
    # id Permet la visualisation dans la fenetre de tkinter
    self.id = canvas.create_image( planet.x,planet.y,image=self.photo)
    # Affiche le nom de la planete juste sous le sprite
    self.text_id = canvas.create_text(
      planet.x, planet.y + 32, # position du texte juste en dessous du sprite
      text=planet.NomP, fill="#EBCCFB"
    )

    
    
class CanvasResize:
  def __init__(self,canvas):
    self.canvas = canvas
    self.canvas.bind("<Configure>", self.resize)
  def resize(self,event):
    # Redimensionne le canvas
    self.canvas.config(width=event.width, height=event.height)

def GalaxyPath(canvas,galaxy):
  col = random.randint(0,0x100000)
  for i in range(len(galaxy)):
      p1 = galaxy[i]
      p2 = galaxy[(i + 1) % len(galaxy)] # pour faire un circuit fermé, on prend le prochain planète 
      canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill=f"#{col:06x}", width=2) # Trace le chemin entre planètes consécutives

class Reglages:
  def __init__(self,root):
    self.root = root
    self.frame = tkr.Frame(root, bg="#7A7A7A", width=200)
    self.frame.pack(side="left", fill="y")

    # Affichage nb de planetes
    nbp = tkr.Label(self.frame, text="Nombre de planètes:", bg="#B3B3B3")
    nbp.pack(anchor="w", padx=10, pady=(10, 2))
    self.planets_spin = tkr.Spinbox(self.frame, from_=1, to=1000, width=8)
    self.planets_spin.pack(anchor="w", padx=10, pady=(0, 10))
    self.planets_spin.delete(0, "end")

    #Affichage nb d'itinéraires
    nbi = tkr.Label(self.frame, text="Nombre d'itinéraires:", bg="#B3B3B3")
    nbi.pack(anchor="w", padx=10, pady=(0, 2))
    self.itineraries_spin = tkr.Spinbox(self.frame, from_=1, to=1000, width=8)
    self.itineraries_spin.pack(anchor="w", padx=10, pady=(0, 10))
    self.itineraries_spin.delete(0, "end")

    #Affichage nombre de générations
    self.generations_label = tkr.Label(self.frame, text="Nombre de générations:", bg="#B3B3B3")
    self.generations_label.pack(anchor="w", padx=10, pady=(0, 2))
    self.generations_spin = tkr.Spinbox(self.frame, from_=1, to=1000, width=8)
    self.generations_spin.pack(anchor="w", padx=10, pady=(0, 10))
    self.generations_spin.delete(0, "end")

    # Bouton pour démarrer la simulation
    self.start_button = tkr.Button(self.frame, text="Démarrer la simulation", bg="#B3B3B3")
    self.start_button.pack(anchor="w", padx=10, pady=(4, 10))

  def get_nbp(self):
    return int(self.planets_spin.get())

  def get_nbi(self):
    return int(self.itineraries_spin.get())

  def start_cmd(self, command):
    self.start_button.config(command=command)