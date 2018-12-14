#!/usr/bin/python3

import random
import pprint

# Nombre de sommets
nSom = 0
# Nombre d'arêtes
mArc = 0
# Matrice d'adjacence
matAdj = []
# Liste d'adjacence
lstAdj = [[], []]


# Procédure de translation d'une matrice d'adjacence en liste d'adjacence
def matToLst():
	global lstAdj

	# Nombre total de successeurs (indice du dernier successeur connu)
	nbFils = -1

	# Pour chaque liste de successeurs d'un sommet
	for lstFils in matAdj:

		premFils = 1
		for indFils in range(len(lstFils)):

			# S'il existe un arc pour ce sommet -> successeur
			if lstFils[indFils] is not 0:

				# On ajoute l'indice du successeur à la liste des successeurs
				lstAdj[1].append(indFils)

				# On incrémente le nombre total de successeurs
				nbFils += 1

				# Si le successeur est le premier de ce sommet
				if premFils:

					# On ajoute son indice à la liste des têtes
					lstAdj[0].append(nbFils)
					premFils = 0

		# Si aucun arc n'existe pour ce sommet
		if premFils:

			# On ajoute l'indice du prochain successeur à la liste des têtes
			lstAdj[0].append(nbFils + 1)


# Procédure de génération de graphe
def randGraph():
	global matAdj

	print("\nGénération du graphe orienté de " + str(nSom) + " sommets et " + str(mArc) + " arcs..")

	matAdj = [[0 for _ in range(nSom)] for _ in range(nSom)]
	mArcRest = mArc
	while mArcRest > 0:
		random.seed()
		numSomOri = random.randint(min(range(nSom)), max(range(nSom)))
		numSomDest = random.randint(min(range(nSom)), max(range(nSom)))
		if matAdj[numSomOri][numSomDest] == 0:
			matAdj[numSomOri][numSomDest] = random.randint(1, 9)
			mArcRest -= 1

	matToLst()


# def varianteBellmanFord():


# Procédure naïve de Dijkstra
def naiveDijkstra():
	p = 0
	v = 0
	M = nSom


# def prioDijkstra():


# def compaDijkstra():


# def johnson():


def main():
	global nSom
	global mArc

	while True:
		nSom = int(input("Saisissez N (nombre de sommets): "))
		mArc = int(input("Saisissez M (nombre d'arcs)    : "))
		if (mArc <= nSom * (nSom - 1)) and (mArc > 0):
			break
		print("Erreur: Nombre d'arcs trop important")

	randGraph()

	print("\nMatrice d'adjacence:")
	pprint.pprint(matAdj)

	print("\nListe d'adjacence:\n[" + str(lstAdj[0]) + ",\n " + str(lstAdj[1]) + "]")


main()
