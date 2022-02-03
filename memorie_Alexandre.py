#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from tkinter import *
# ----- zone de définition des variables -------------------------------

coup=0

# init matrice jeu
nb_lignes, nb_colonnes = 5, 6
nb_total_cartes = nb_lignes * nb_colonnes

# ----- zone de définition des fonctions -------------------------------


def initialisation_du_jeu ():

    global delai
    global nb_cartes_trouvees, liste_id_cartes, cartes_melangees,coup,record
    
    coup=-1
    
    recup()
    
    Lrecord=Label(fenetre,text="record: "+str(record)+"  ")
    Lrecord.place(x=165,y=560)

    # délai affichage cartes fixé(en ms)
    delai =random.choice([500])

    # initialisation d'une variable
    nb_cartes_trouvees = 0

    # affiche le dos des cartes
    # crée une liste d'identifiants de cartes sur le canevas
    liste_id_cartes = initialisation_du_canevas()
    

    # crée une liste aléatoire de 30 nombres entre 1 et 15 apparaissant deux fois chacun 
    cartes_melangees = melanger_cartes()

    # réinitialisation de la souris 
    réinitialisation_du_clics_souris()



def initialisation_du_canevas ():
    #remplissage du canevas avec des dos de cartes

    # on efface le canevas
    canvas.delete(ALL)

    # initialisation liste des identifiants de cartes
    liste_ids = []

    # on parcourt les lignes
    for ligne in range(nb_lignes):

        # on parcourt les colonnes
        for colonne in range(nb_colonnes):

            # on met en place les dos de cartes et on en profite pour "marquer" les cartes (tags)
            liste_ids.append(canvas.create_image(110*colonne+10, 110*ligne+10,anchor=NW, image=dos_carte, tags="cartes",))

    return liste_ids



def charger_images ():
    #mise en mémoire des images des cartes à jouer

    # l'image no 0 est le dos des cartes
    # le nombre d'image est définie par la moitié des carte plus le dos 
    nb_images = 1 + nb_total_cartes // 2
    
    #création de la liste des images
    images = []

    # on importe les images en mémoire
    # de 1 à 15
    for i in range(nb_images):

        # on ajoute une nouvelle image à la liste
        images.append(PhotoImage(file="im{}.gif".format(i)))  

    return images


def melanger_cartes ():
    #création d'une liste d'indices de cartes mélangés

    # liste des indices de cartes
    liste = list(range(1, nb_total_cartes//2 + 1)) * 2

    # on mélange les indices de cartes
    random.shuffle(liste)

    return liste



def masquer_cartes ():
    #on retourne toutes les cartes du canevas
    
    #on affecte l'image du dos de carte à toute les images (tag"carte")
    canvas.itemconfigure("cartes", image=dos_carte)
    
    # réinitialisation de la souris
    réinitialisation_du_clics_souris()


def supprimer_cartes ():
    "on supprime les cartes qui matchent"

    global nb_cartes_trouvees

    # suppression cartes 1 et 2
    canvas.delete(id_carte1)
    canvas.delete(id_carte2)

    # augmentation du nombre de cartes trouvées
    nb_cartes_trouvees += 2

    # la partie est-elle terminée ?
    if nb_cartes_trouvees >= nb_total_cartes:

        # fin de partie
        win()

    # non, on continue de jouer
    else:

        # réinitialisation de la souris
        réinitialisation_du_clics_souris()



def win ():
    #victoire
    
    global record,coup
    
    coup=coup+1
    
    L=Label(fenetre,text="vous avez joué "+ str(coup)+ " coups!  ")
    L.place(x=1,y=560)
   

    # on efface d'abord le canevas
    canvas.delete(ALL)

    # point central du canevas
    x, y = canvas.winfo_reqwidth()//2, canvas.winfo_reqheight()//2

    # on affiche un le message de victoire
    canvas.create_text(x, y-40,text="BRAVO !",font="sans 32 bold",fill="blue")
    canvas.create_text(x, y,text="Bien joué vous avez gagné en " +str(coup)+ " coups!",font="sans 16 bold",fill="dark blue")
    
    # bouton rejouer
    canvas.create_window(x, y+40,window=Button(canvas, text="Rejouer",font="sans 16 bold",command=initialisation_du_jeu),)
    
    #test du record
    if coup<record and nb_total_cartes<30 :
        
        #le record n'est pas compté car mode facile
        #label du record non compté
        canvas.create_text(x, y+80,text="Les records ne sont pas compté en mode facile",font="sans 16 bold",fill="dark blue")
     
    #test du record 
    if coup<record and nb_total_cartes>29 :
        
        #conservation du record car mode normal
        record=coup
        
        #label du record
        canvas.create_text(x, y+80,text=" C'est un nouveau record!!!",font="sans 16 bold",fill="dark blue")
    
    #enregistrement du record dans le fichier
    fichier=open("record .txt","w")
    fichier.write(str(record))
    
    #récuperation du record
    fichier=open("record .txt","r")
    
    for ligne in fichier:
        Liste.append(ligne.replace("\n",""))
        
    record=int(Liste[0])


def réinitialisation_du_clics_souris ():

    global id_carte1, id_carte2,coup
    
    #remise à 0 des deux variable des carte retourné
    id_carte1 = id_carte2 = 0
    
    #aumentation du nombre de coups
    coup=coup+1
    
    # création du Label indiquant le nombre de coup joué
    L=Label(fenetre,text="vous avez joué "+ str(coup)+ " coups!  ")
    L.place(x=1,y=560)
    




def clic_souris (event):

    global id_carte1, id_carte2
    

    # init coordonnées clic souris
    x, y = event.x, event.y

    # recherche de carte retourne la liste des id d'item dans x y x y c'est à dire une carte
    collisions = canvas.find_overlapping(x, y, x, y)

    # le joueur a cliqué sur une carte ?
    if collisions and collisions[0] in liste_id_cartes:
        

        # init ID carte
        id_carte = collisions[0]
        

        # première carte à été retourner ?
        if id_carte1 == 0:

            # init IDs cartes
            id_carte1 = id_carte
            id_carte2 = 0

            afficher_carte(id_carte1)

        # deuxième carte à été retourner ?
        elif id_carte2 == 0 and id_carte != id_carte1:

            # init ID carte
            id_carte2 = id_carte

            afficher_carte(id_carte2)

            # correspondance trouvée ?
            if correspondance(id_carte1, id_carte2):

                # supprimer les cartes au bout du délai prédéfini
                fenetre.after(delai, supprimer_cartes)

            # pas de correspondance trouvée
            else:

                # retourner les cartes au bout d'un délai
                fenetre.after(delai, masquer_cartes)




def afficher_carte (id_carte):
    
    #affiche la carte qui correspond à l'ID de canvasIte
    canvas.itemconfigure(id_carte, image=images[valeur_carte(id_carte)])



def valeur_carte (id_carte):
    #retourne la valeur de la carte correspondant à l'ID de canvasItem

    # init index carte
    index = liste_id_cartes.index(id_carte)

    # valeur carte à cet emplacement
    return cartes_melangees[index]



def correspondance (id1, id2):
    
    #vérifie la correspondance entre deux valeurs de cartes
    return bool(valeur_carte(id1) == valeur_carte(id2))

def recup():
    global record
    
    #création d'une liste vide
    Liste=[]
    
    #ouverture du fichier avec le record enregistré
    fichier=open("record .txt","r")
    
    #récupération du record
    for ligne in fichier:
        Liste.append(ligne.replace("\n",""))
        
    record=int(Liste[0])
    
def facile() :
    global nb_colonnes,nb_lignes,nb_total_cartes
    
    #changement du nombre de carte
    nb_lignes, nb_colonnes = 5, 4
    
    nb_total_cartes = nb_lignes * nb_colonnes
    
    initialisation_du_jeu()

def difficile():
    global nb_colonnes,nb_lignes,nb_total_cartes
    
    #changement du nombre de carte
    nb_lignes, nb_colonnes = 5, 6
    
    nb_total_cartes = nb_lignes * nb_colonnes
    print(nb_lignes, nb_colonnes,nb_total_cartes)
    
    initialisation_du_jeu()   


# ----- Programme principal --------------------------------------------

# fenêtre principale
fenetre = Tk()
fenetre.title("Memory")
fenetre.resizable(width=False, height=False)

#récupération du record
recup()

# la liste images contient
# les 11 images (dos + 10 images)
images = charger_images()

# init dos carte
dos_carte = images[0]

# init canevas graphique
canvas = Canvas(fenetre, width=850, height=550)
canvas.pack()

# init données jeu
initialisation_du_jeu()

# fonction associé au clics souris
canvas.bind('<Button-1>', clic_souris)

# bouton quitter
Quiter=Button(fenetre,text="Quitter",command=fenetre.destroy,bg="black",fg="white").pack(side=RIGHT, padx=5, pady=5)

# Bouton recommencer    
Recommencer=Button(fenetre,text='Recommencer',command=initialisation_du_jeu)
Recommencer.place(x=260,y=557)

#Bouton mode normal
Difficile=Button(fenetre,text='Mode normal(30 cartes)',command=difficile,bg="dark red",fg="white",highlightbackground="black")
Difficile.place(x=670,y=200)

#bouton mode facile
Facile=Button(fenetre,text='Mode facile(20 cartes)',command=facile,bg="dark blue",fg="white",highlightbackground="black")
Facile.place(x=670,y=100)

#instrucion
Aide=Label(fenetre,text="TROUVE TOUTES LES PAIRES!!",fg="green")
Aide.place(x=670,y=10)


# boucle principale
fenetre.mainloop()
