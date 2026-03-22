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


def draw_tagged_ga_path(chemin):
    # Appelle la fonction centralisee dans graphics puis tag les lignes ajoutees
    before_items = set(canvas.find_all())
    graphics.GalaxyPath(canvas, chemin)
    after_items = set(canvas.find_all())
    new_items = after_items - before_items
    for item_id in new_items:
        if canvas.type(item_id) == "line":
            canvas.addtag_withtag("ga_path", item_id)




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

        if len(fitness_list) < 2:
            break

        # Selection des meilleurs itinerares selon le score du tournoi
        ranked_idx = sorted(range(len(score)), key=lambda i: score[i], reverse=True)
        n_parents = min(4, len(ranked_idx))
        parents = [fitness_list[i][0] for i in ranked_idx[:n_parents]]

        # Croisement jusqu'a recreer toute la population
        enfants = []
        while len(enfants) < nbi:
            if len(parents) >= 2:
                p1, p2 = rd.sample(parents, 2)
            else:
                p1 = parents[0]
                p2 = parents[0]
            enfants.append(ittest.croisement(p1, p2))

        ittest.itinerarios = enfants

        # Mutation legere pour maintenir la diversite genetique
        #ittest.mutation(0.1)

        best_gen_i = ranked_idx[0]
        print(
            f"distance={fitness_list[best_gen_i][2]:.2f}"
        )
        # effacer et redessiner le chemin gagnant pour chaque gen 
        canvas.delete("ga_path")
        draw_tagged_ga_path(fitness_list[best_gen_i][0])
        canvas.update_idletasks()
        canvas.update()
        canvas.after(50)
        

    # resultat final 
    final_tournoi = classes.Tournoi()
    final_fitness = final_tournoi.fitness(ittest)
    best_chemin, _, best_dist = max(final_fitness, key=lambda x: x[1])
    canvas.delete("ga_path")
    draw_tagged_ga_path(best_chemin)
    print(f"\nmeilleur itineraire final: distance={best_dist:.2f}")
    


boite_reglages.start_cmd(start_simulation)


root.mainloop() # hace correr el programa no se debe de poner nada despues de esta linea segun stack overflow porque si no el programa lo ignorara