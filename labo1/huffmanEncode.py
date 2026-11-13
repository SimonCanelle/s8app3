import numpy as np


def calcEntropie(liste, total):
    somme = 0
    for item in liste:
        prob = item[1]/total
        somme+= prob * np.log2(prob)

    return somme * -1

def 


liste = [["A",10],["B",10],["C",20],["D",30],["E",50],["F",50],["G",80]]
total = 250

print(f"entropie = {calcEntropie(liste, total)}")



