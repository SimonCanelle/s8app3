###
# Auteur(s)   : Simon Janelle-Bombardier et William Parent
# Date        : 2026-11-13
# Description : Comparaison de 3 méthode d'encodage entropique. RLC vs Arithmétique vs Huffman
###


import os
import cv2 as cv

RESSOURCE_PATH = "./ressources"

# lis un fichier dans le dossier de ressources du nom <nomFichier> et renvoie les données
def lectureFichier(nomFichier, type):#ajouter arg type pour fichier txt vs image?
    FP = os.path.join(RESSOURCE_PATH, nomFichier)
    
    if (type == "img"):
        data = cv.imread(FP)

    elif (type == "txt"):
        with open(FP, "r") as f:
            data = f.read()

    else:
        raise("File type not supported")

    return data


# enregistre les données dans un fichier du nom donné
def enregistreFichier(binString, nomFichier):
    pass

# analyse les statistique d'une images et les packages dans un dictionnaire
def analyseStatistiqueImage(image):
    pass

# analyse les statistique de données encodées et les packages dans un dictionnaire
def analyseStatistiqueEncode(encData):
    pass

# calcule l'entropie d'une série de symbole
def calculeEntropie(data, stats):
    pass

# encode les données en une binary string
def encode(methode, data, stats):
    if methode == "rlc":
        pass
    elif methode == "huffman":
        pass
    elif methode == "arithmetique":
        pass
    else:
        raise("type d'encodage non supporté")

#retourne un tableau de données 
def decode(methode, data):
    if methode == "rlc":
        pass
    elif methode == "huffman":
        pass
    elif methode == "arithmetique":
        pass
    else:
        raise("type d'encodage non supporté")
    

# compare les statistique des images sources avec 
def calculDebitBinaire(srcStats, encStats):
    pass

# compare une image source avec sa version décodé
# retourne vrai si elle sont identique (ce qu'on veut avec lossless comp)
def verificationEncode(srcImg, decImg):
    pass

if __name__ == "__main__":
    print("hello world")


