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
    nbg = boite_reglages.get_nbg()
    nbr = boite_reglages.get_nbr()

    galaxie = classes.Galaxie() # iniciar la galaxia
    galaxie.SamsungGalaxy(nbp) # generar los planetas
    sprites = []
    for planet in galaxie.listPlnt:
        sprites.append(graphics.PlanetSprite(canvas, planet, f"Assets/planete_{rd.randint(1,8)}.png"))
        print(planet)
    etat_sim_graph["sprites"] = sprites

    ittest = classes.Itineraires(galaxie)
    ittest.genererRd(nbi)

    # Algorithme genetique: on fait evoluer la population pendant nbg generations
    for generation in range(nbg):
        ttest = classes.Tournoi()
        fitness_list = ttest.fitness(ittest)
        score = ttest.tournoi(rounds=nbr)

        #arrete si pas assez des itineraires pour faire tournoi
        if len(fitness_list) < 2:
            break

        # Selection des meilleurs itinerares selon le score du tournoi
        ranked_idx = sorted(range(len(score)), key=lambda i: score[i], reverse=True)#
        # selection des 4 (ou  moins si pop <4) meilleurs
        n_parents = min(4, len(ranked_idx))
        parents = [fitness_list[i][0] for i in ranked_idx[:n_parents]]
       
        #ELITISME
        elite = []# des fois il ya des itineraires qui sont tres bien fait dcp on les garde et on les donnera à l'enfant
        if(len(ranked_idx) > 1 ):# si on plus de 2 itinéraires on prend le top2
           elite = [fitness_list[ranked_idx[0]][0], fitness_list[ranked_idx[1]][0]] 
        else:# sinon juste on prend l'unique itinéraire
            elite = [fitness_list[ranked_idx[0]][0]]
            
        # Croisement jusqu'a recreer toute la population
        enfants = elite[:] # [:] signifca que copia todo el tableau es decirt que enfat es igual a tod elite es como usar copy
        while len(enfants) < nbi:
            if len(parents) >= 2:
                p1, p2 = rd.sample(parents, 2)
            else:# si il y a qu'un seul parent, il se croise à lui même
                p1 = parents[0]
                p2 = parents[0]
            enfants.append(ittest.croisement(p1, p2))

        ittest.itinerarios = enfants# al final tenemos en enfant elite mas la nueva gen

        # Mutation legere pour maintenir la diversite genetique
        ittest.mutation(0.2)

        best_gen_i = ranked_idx[0]
        print(
            f"Top generation {generation + 1}: "
            f"distance={fitness_list[best_gen_i][2]:.2f}"
            f" | score={score[best_gen_i]}"
        )
        # effacer et redessiner le chemin gagnant pour chaque gen 
        canvas.delete("chemin_gen_i")
        graphics.tagged_path(canvas, fitness_list[best_gen_i][0])
        canvas.update_idletasks()
        canvas.update()
        canvas.after(50)
        if generation == 1:
            canvas.after(2000) # pause pour voir le gagnant initial
        

    # resultat final 
    final_tournoi = classes.Tournoi()
    final_fitness = final_tournoi.fitness(ittest)
    best_chemin, _, best_dist = max(final_fitness, key=lambda x: x[1])
    canvas.delete("chemin_gen_i")
    graphics.tagged_path(canvas,best_chemin)
    print(f"\nmeilleur itineraire final: distance={best_dist:.2f}")
    print("ordre des planetes du meilleur itineraire final:")
    for planet in best_chemin:
        print(planet)
    print("=====simulation terminee=====")
        
boite_reglages.start_cmd(start_simulation)


root.mainloop() # hace correr el programa no se debe de poner nada despues de esta linea porque si no el programa lo ignorara