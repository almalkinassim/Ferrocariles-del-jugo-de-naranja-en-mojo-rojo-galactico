import classes
import graphics 
import tkinter as tkr
import random as rd

#interface graphique
root = tkr.Tk()
root.title("Ferrocariles del jugo de naranja en mojo rojo galactico")
canvas = tkr.Canvas(root, width=1240, height=786, bg= "#2F1939")
boite_reglages = graphics.Reglages(root)
canvas.pack()

# garde les sprites pour eviter qu'ils soient garbage collected et disparaissent de l'affichage
etat_sim_graph = {"sprites": []}

#boucle pour chaque generation 
def start_simulation():
    canvas.delete("all") # reinitialise le canvas
    
    nbp = boite_reglages.get_nbp() 
    nbi = boite_reglages.get_nbi() 
    #nbg = boite_reglages.get_nbg() #remettre apres avoir fait la partie generations

    galaxie = classes.Galaxie() # iniciar la galaxia
    galaxie.SamsungGalaxy(nbp) # generar los planetas
    sprites = []
    for planet in galaxie.listPlnt:
        sprites.append(graphics.PlanetSprite(canvas, planet, f"Assets/planete_{rd.randint(1,8)}.png"))
        print(planet)
    etat_sim_graph["sprites"] = sprites
    

    ittest = classes.Itineraires(galaxie) # test de itinerarios
    ittest.genererRd(nbi) # generer les itinéraires

    for i in range(nbi):
        graphics.GalaxyPath(canvas, ittest.itinerarios[i])
        print("distance itinéraire", i, ":", ittest.Dist(ittest.itinerarios[i]))
boite_reglages.start_cmd(start_simulation)

root.mainloop() # hace correr el programa no se debe de poner nada despues de esta linea segun stack overflow porque si no el programa lo ignorara