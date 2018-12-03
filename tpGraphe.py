#!/usr/bin/python
import os
import sys

def graphAlea(n,m):
	if(n<m):
		print("Erreur, M est plus grand que N")
	else:
		print("Saisie Valide !")

def main():
	n = input("Saisissez N : ")
	m= input("Saisissez M : ")
	graphAlea(n,m)


main()