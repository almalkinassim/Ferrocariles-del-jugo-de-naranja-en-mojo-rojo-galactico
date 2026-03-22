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
    nbg = boite_reglages.get_nbg() #remettre apres avoir fait la partie generations


    galaxie = classes.Galaxie() # iniciar la galaxia
    galaxie.SamsungGalaxy(nbp) # generar los planetas
    sprites = []
    for planet in galaxie.listPlnt:
        sprites.append(graphics.PlanetSprite(canvas, planet, f"Assets/planete_{rd.randint(1,8)}.png"))
        print(planet)
    etat_sim_graph["sprites"] = sprites
   


    ittest = classes.Itineraires(galaxie) # test de itinerarios
    ttest = classes.Tournoi()
    ittest.genererRd(nbi) # generer les itinéraires


    for i in range(nbi):
        graphics.GalaxyPath(canvas, ittest.itinerarios[i])
        print("distance itinéraire", i, ":", ittest.Dist(ittest.itinerarios[i]))
     


    fitness_list = ttest.fitness(ittest)
    score = ttest.tournoi(rounds=20)
    parents = []
    enfants = []
    peores = []

    #elije a l os mejores
    for i in range(4):
        i = score.index(max(score))
        parents.append(fitness_list[i][0])
        chemin, fitness, dist = fitness_list[i]
        print(f"Itin {i} -> score={score[i]}")

        score[i] = -1
    #elije los peores    
    for i in range(4):
        j = score.index(min(score))
        peores.append(fitness_list[i][0])
        chemin, fitness, dist = fitness_list[i]
        print(f"Itin {i} -> score={score[i]}")
        score[j] = +1
   
    for i in range(len(ittest.itinerarios)):
        p1, p2 = rd.sample(parents, 2)
        enfant = ittest.croisement(p1, p2)
        enfants.append(enfant)
    ittest.itinerarios = enfants




    parent1 = fitness_list[0][0]
    parent2 = fitness_list[1][0]


    enfant = ittest.croisement(parent1, parent2)


    print("\n--- TEST CROISEMENT ---")
    print("Parent 1 :", parent1)
    print("Parent 2 :", parent2)
    print("Enfant   :", enfant)
    print("Peores   :", peores)
    #galaxie.listPlnt.remove(peores)
    galaxie.listPlnt.append(enfant)
    


boite_reglages.start_cmd(start_simulation)


root.mainloop() # hace correr el programa no se debe de poner nada despues de esta linea segun stack overflow porque si no el programa lo ignorara