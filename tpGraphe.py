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

	for som in matAdj:
		fstSucc = 1
		for suc in som:
			if suc is not 0:
				lstAdj[1].append(suc)
				if fstSucc:
					lstAdj[0].append(len(lstAdj[1]) - 1)
					fstSucc = 0


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


def main():
	global nSom
	global mArc

	inpUt = False

	while not inpUt:
		nSom = int(input("Saisissez N (nombre de sommets): "))
		mArc = int(input("Saisissez M (nombre d'arcs)    : "))
		if mArc <= nSom * (nSom - 1):
			break
		print("Erreur: Nombre d'arcs trop important")

	randGraph()

	print("\nMatrice d'adjacence:")
	pprint.pprint(matAdj)

	print("\nListe d'adjacence:\n[" + str(lstAdj[0]) + ",\n " + str(lstAdj[1]) + "]")

main()
