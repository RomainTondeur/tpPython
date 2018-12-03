#!/usr/bin/python3
import os
import sys

def graphAlea(n,m):
	sumN = n*(n-1)
	if m > sumN :
		print("Erreur, M est plus grand que N")
	else:
		print("Saisie Valide !")

def main():
	n = input("Saisissez N : ")
	m = input("Saisissez M : ")
	graphAlea(n,m)


main()