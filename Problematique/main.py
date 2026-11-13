###
# Auteur(s)   : Simon Janelle-Bombardier et William Parent
# Date        : 2026-11-13
# Description : Comparaison de 3 méthode d'encodage entropique. RLC vs Arithmétique vs Huffman
###


import os
import cv2 as cv
import numpy as np

RESSOURCE_PATH = "Problematique\\ressources"


# lis un fichier dans le dossier de ressources du nom <nomFichier> et renvoie les données
def lectureFichier(nomFichier, type):#ajouter arg type pour fichier txt vs image?
    FP = os.path.join(RESSOURCE_PATH, nomFichier)
    try:
        #lecture d'image
        if (type == "img"):
            data = cv.imread(FP, cv.IMREAD_GRAYSCALE)            
        #lecture de texte
        elif (type == "txt"):
            with open(FP, "r") as f:
                data = f.read()
        #type non supporté
        else:
            raise("File type not supported")

        if data is None :
            raise("Error reading data")
    
    except Exception as e:
        raise(e)

    return data


# enregistre une binary string dans un fichier texte du nom donné
def enregistreFichier(binString, nomFichier):
    FP = os.path.join(RESSOURCE_PATH, nomFichier)
    with open(FP, "w+") as f:
        f.write(binString)

    
# analyse les statistique d'une images et les packages dans un dictionnaire
def analyseStatistiqueImage(image:list[int]):
    statDict = dict()
    statDict["min"] = np.min(image)
    statDict["max"] = np.max(image)
    statDict["mean"] = np.mean(image)
    statDict["std"] = np.std(image)
    symbolDict = dict()
    image1d = [item for sublist in image for item in sublist]
    for 

    



# analyse les statistique de données encodées et les packages dans un dictionnaire
def analyseStatistiqueEncode(encData):
    pass


# calcule l'entropie d'une série de symbole
def calculeEntropie(data, stats):
    pass


# encode les données en une binary string (inclu les métadonnées)
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
    #1. lecture des images
    img0 = lectureFichier("source0.jpg", "img")
    img1 = lectureFichier("source1.jpg", "img")
    img2 = lectureFichier("source2.jpg", "img")
    img3 = lectureFichier("source3.jpg", "img")
    imgs = [{"image":img0}, {"image":img1}, {"image":img2}, {"image":img3}]

    #2. analyse statistiques
    for img in imgs:
        img["statistiques"] = analyseStatistiqueImage(img["image"])

    #3. calculs d'entropie
    #4. encodage avec les 3 méthodes
    #5. enregistrement des données d'encodage
    #6. lecture des fichiers encodé
    #7. décodage des images
    #8. vérification des images
    #9. analyses statistiques des encodeurs




