#!/usr/bin/python3

import random
import math
import heapq
import time


def initMain():
    while True:
        nbSommets = int(input("Saisissez N (nombre de sommets): "))
        nbArcs = int(input("Saisissez M (nombre d'arcs): "))
        minPond = int(input("Saisissez le minimum de la pondération des arcs: "))
        maxPond = int(input("Saisissez le maximum de la pondération des arcs: "))
        indSommet = random.randint(min(range(nbSommets)), max(range(nbSommets)))
        if (nbArcs <= nbSommets * (nbSommets - 1)) and (nbArcs > 0):
            return nbSommets, nbArcs, minPond, maxPond, indSommet
        print("Erreur: Nombre d'arcs trop important")


# Procédure de génération d'un graphe (matrice d'adjacence)
def randGraph(nbSommets, nbArcs, minPond, maxPond):

    print("\nGénération du graphe orienté de " + str(nbSommets) + " sommets et " + str(nbArcs) + " arcs..")

    # Matrice d'adjacence
    matrice = [[0 for _ in range(nbSommets)] for _ in range(nbSommets)]
    mArcRests = nbArcs
    while mArcRests > 0:
        random.seed()
        numSomOri = random.randint(min(range(nbSommets)), max(range(nbSommets)))
        numSomDest = random.randint(min(range(nbSommets)), max(range(nbSommets)))
        if not matrice[numSomOri][numSomDest]:
            matrice[numSomOri][numSomDest] = random.randint(minPond, maxPond)
            mArcRests -= 1

    return matrice


# Procédure de translation d'une matrice d'adjacence en liste d'adjacence
def matToLst(matrice):

    # Liste d'adjacence
    liste = [[],[]]

    # Nombre total de successeurs (indice du dernier successeur connu)
    nbFils = -1

    # Pour chaque liste de successeurs d'un sommet
    for lstFils in matrice:

        premFils = 1
        for indFils in range(len(lstFils)):

            # S'il existe un arc pour ce sommet -> successeur
            if lstFils[indFils] is not 0:

                # On ajoute l'indice du successeur à la liste des successeurs
                liste[1].append([indFils, lstFils[indFils]])

                # On incrémente le nombre total de successeurs
                nbFils += 1

                # Si le successeur est le premier de ce sommet
                if premFils:

                    # On ajoute son indice à la liste des têtes
                    liste[0].append(nbFils)
                    premFils = 0

        # Si aucun arc n'existe pour ce sommet
        if premFils:

            # On ajoute l'indice du prochain successeur à la liste des têtes
            liste[0].append(nbFils + 1)
    return liste


# Procédure de retour de la liste des successeurs d'un sommet donné
def lstFilsSommet(liste, indSommet):
    if 0 < indSommet < len(liste[0])-1:
        if liste[0][indSommet] == liste[0][indSommet+1]:
            return []
        return liste[1][liste[0][indSommet]:liste[0][indSommet+1]]
    elif indSommet == 0:
        return liste[1][:liste[0][indSommet+1]]
    elif indSommet == len(liste[0])-1:
        if liste[0][indSommet] == len(liste[1]):
            return []
        return liste[1][liste[0][indSommet]:]


def bellmanFord(liste, indSommet):
    meilDistance = [math.inf for _ in range(len(liste[0]))]
    meilDistance[indSommet] = 0
    cpMeilDistance = meilDistance

    for _ in range(len(liste[0]) - 1):

        # Pour chaque liste de successeurs d'un sommet
        for indSom in range(len(liste[0])):
            fils = lstFilsSommet(liste, indSom)
            if len(fils) > 0:
                for successeur in fils:

                    # Recherche du plus petit coût
                    if meilDistance[indSom] + successeur[1] < meilDistance[successeur[0]]:
                        meilDistance[successeur[0]] = meilDistance[indSom] + successeur[1]

        if cpMeilDistance == meilDistance:
            break
        else:
            cpMeilDistance = meilDistance

    for _ in range(len(liste[0]) - 1):

        # Pour chaque liste de successeurs d'un sommet
        for indSom in range(len(liste[0])):
            fils = lstFilsSommet(liste, indSom)
            if len(fils) > 0:
                for successeur in fils:

                    # Recherche d'absorbsion
                    if meilDistance[indSom] + successeur[1] < meilDistance[successeur[0]]:
                        meilDistance[successeur[0]] = -math.inf
                        print("\nAttention: Circuit absorbant détecté")
                        return meilDistance

    return meilDistance


# Procédure de recherche du tuple minimum du tas binaire
def minimum(tasBinaire):
    index, minPond = tasBinaire[0][0], tasBinaire[0][1]
    for combinaison in tasBinaire:
        if combinaison[1] < minPond:
            index, minPond = combinaison[0], combinaison[1]
    return [index, minPond]


# Procédure naïve de Dijkstra
def naiveDijkstra(liste, indSommet):
    visite = [0 for _ in range(len(liste[0]))]
    meilDistance = [math.inf for _ in range(len(liste[0]))]
    meilDistance[indSommet] = 0
    tasBinaire = [[indSommet, 0]]

    while len(tasBinaire) != 0:
        index, minPond = minimum(tasBinaire)
        tasBinaire.pop(tasBinaire.index(minimum(tasBinaire)))
        visite[index] = 1
        fils = lstFilsSommet(liste, index)
        if len(fils) > 0:
            for successeur in fils:
                if visite[successeur[0]]:
                    break
                if meilDistance[index] + successeur[1] < meilDistance[successeur[0]]:
                    meilDistance[successeur[0]] = meilDistance[index] + successeur[1]
                    tasBinaire.append([successeur[0], meilDistance[index] + successeur[1]])
    return meilDistance


# Procédure prioritaire de Dijkstra
def prioDijkstra(liste, indSommet):
    visite = [0 for _ in  range(len(liste[0]))]
    meilDistance = [math.inf for _ in range(len(liste[0]))]
    meilDistance[indSommet] = 0
    tasBinaire = [[indSommet, 0]]
    heapq.heapify(tasBinaire)

    while len(tasBinaire) != 0:
        index, minPond = heapq.heappop(tasBinaire)
        visite[index] = 1
        fils = lstFilsSommet(liste, index)
        if len(fils) > 0:
            for successeur in fils:
                if visite[successeur[0]]:
                    break
                if meilDistance[index] + successeur[1] < meilDistance[successeur[0]]:
                    meilDistance[successeur[0]] = meilDistance[index] + successeur[1]
                    heapq.heappush(tasBinaire, ([successeur[0], meilDistance[index] + successeur[1]]))
    return meilDistance


def johnson(liste, nbArcs):
    for ind in range(len(liste[0])):
        liste[1].append([ind, 0])
    liste[0].append(nbArcs)

    bellDistance = bellmanFord(liste, len(liste[0]) - 1)

    for index in range(len(liste[0])):
        fils = lstFilsSommet(liste, index)

        if len(fils) > 0:
            for successeur in fils:
                liste[1][liste[0][index]][1] = liste[1][liste[0][index]][1] + bellDistance[index] - bellDistance[liste[1][liste[0][index]][0]]

    liste[1] = liste[1][:(-(len(liste[1])-nbArcs)-1)]
    liste[0] = liste[0][:-1]

    meilDistance = [[] for _ in range(len(liste[0]))]

    for ind in range(len(liste[0])):
        meilDistance[ind] = prioDijkstra(liste, ind)

    for indx in range(len(liste[0])):
        for indy in range(len(liste[0])):
            meilDistance[indx][indy] += bellDistance[indy] - bellDistance[indx]

    for index in range(len(liste[0])):
        fils = lstFilsSommet(liste, index)

        if len(fils) > 0:
            for successeur in fils:
                liste[1][liste[0][index]][1] = liste[1][liste[0][index]][1] + bellDistance[liste[1][liste[0][index]][0]] - bellDistance[index]

    return meilDistance


def main():
    # Nombre de sommets et d'arcs
    nbSommets, nbArcs, minPond, maxPond, indSommet = initMain()

    # Matrice d'adjacence
    matriceAdjacence = randGraph(nbSommets, nbArcs, minPond, maxPond)

    # print("\nMatrice d'adjacence:")
    # pprint.pprint(matriceAdjacence)

    # Liste d'adjacence
    listeAdjacence = matToLst(matriceAdjacence)

    print("\nListe d'adjacence:\n[" + str(listeAdjacence[0]) + ",\n " + str(listeAdjacence[1]) + "]")

    # print("\nListe des successeurs du sommet " + str(indSommet) + ":")
    # pprint.pprint(lstFilsSommet(listeAdjacence, indSommet))

    tempsExec = int(time.time()*1000)

    # Liste des coûts en distance pour le sommet indSommet
    lstDistBell = bellmanFord(listeAdjacence, indSommet)

    tempsExec = int(time.time()*1000) - tempsExec

    print("\nBellman-Ford - Sommet " + str(indSommet) + " | " + str(tempsExec) + " ms")
    #pprint.pprint(lstDistBell)

    tempsExec = int(time.time()*1000)

    # Liste des coûts en distance pour le sommet indSommet
    lstDistDijNa = naiveDijkstra(listeAdjacence, indSommet)

    tempsExec = int(time.time()*1000) - tempsExec

    print("\nDijkstra Naïf - Sommet " + str(indSommet) + " | " + str(tempsExec) + " ms")
    #pprint.pprint(lstDistDijNa)

    tempsExec = int(time.time()*1000)

    # Liste des coûts en distance pour le sommet indSommet
    lstDistDijPrio = prioDijkstra(listeAdjacence, indSommet)

    tempsExec = int(time.time()*1000) - tempsExec

    print("\nDijkstra Prioritaire - Sommet " + str(indSommet) + " | " + str(tempsExec) + " ms")
    #pprint.pprint(lstDistDijPrio)

    tempsExec = int(time.time()*1000)

    #
    lstDistJohn = johnson(listeAdjacence, nbArcs)

    tempsExec = int(time.time()*1000) - tempsExec

    print("\nJohnson | " + str(tempsExec) + " ms")

main()
