###
# Auteur(s)   : Simon Janelle-Bombardier et William Parent
# Date        : 2026-11-13
# Description : Comparaison de 3 méthode d'encodage entropique. RLC vs Arithmétique vs Huffman
###


import os
import cv2 as cv
import numpy as np
import copy

#import des fichiers d'encodages
import huffman
import rlc
import arithmetique
from sizeStd import *

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
    statDict["minimum"] = np.min(image)
    statDict["maximum"] = np.max(image)
    statDict["moyenne"] = np.mean(image)
    statDict["ecart-type"] = np.std(image)
    
    symboleStats = np.unique(image, return_counts=True) #retourne les symboles unique et leurs compte    
    symboleStats = [symboleStats[0], symboleStats[1], np.zeros(symboleStats[0].size)] #conversion de tuple a liste pour futur calculs
    nPixel = len(image) * len(image[0])
    for i, car in enumerate(symboleStats[0]): 
         symboleStats[2][i] = symboleStats[1][i]/nPixel      

    statDict["symboles"] = symboleStats #symbole[0] : caractère, symbole[1] : occurences, symbole[2]: propabilité
    
    return statDict

    
# analyse les statistique de données encodées et les packages dans un dictionnaire
def analyseStatistiqueEncode(encData):
    #TODO coder l'analyse statistique des données encodées
    pass


# calcule l'entropie d'une série de symbole
def calculeEntropie(statsDict):
    entropie = 0
    for prob in statsDict["symboles"][2]:
        entropie += prob * np.log2(prob)
    entropie *= -1
    return entropie

# génère les métadonnées et construit la binary string à enregistrer 
def genereBinString(imgs):
    bitString = encodeEntete(imgs)
    for img in imgs:
        bitString += img["encoded"]    
    return bitString

# encode les données en une binary string (inclu les métadonnées)
# data est un dictionnaire contenant:
#   - image : array de données de l'image
#   - encodage : string du type d'encodage
#   - entropie : float bit/symbole théorique
#   - statistiques : dictionnaire de stats
#       - minimum : float
#       - maximum : float
#       - moyenne : float
#       - ecart-type : float
#       - symboles : liste des stats pour chaque symbole
#           - 0 : liste des symbole unique
#           - 1 : liste des occurences des symbole 
#           - 2 : liste des probabilité des symboles
#   - encoded : binstring de l'image encodé 
def encode(methode, data):
    if methode == "rlc":
        data["encoded"] = rlc.encode(data)
        data["encodage"] = "rlc"
    elif methode == "huffman":
        data["encoded"] = huffman.encode(data)
        data["encodage"] = "huffman"
    elif methode == "arithmetique":
        data["encoded"] = arithmetique.encode(data)
        data["encodage"] = "arithmetique"
    else:
        raise("type d'encodage non supporté")

# calcule les métadonnées à mettre dans l'entête 
#TODO vérifier que les données 
# retourne une liste #[nombre d'image:8b, type encodage:2b, longueur de données encodées:24b] #16,777,216 max element in encoded
def encodeEntete(data):
    entete = format(len(data), "08b")
    for img in data:
        if img == "rlc":
             entete += format(0, "02b")
        elif img == "huffman":
            entete += format(1, "02b")
        elif img == "arithmetique":     
            entete += format(2, "02b")
        entete += format(len(img["encoded"]), "024b")
    return entete

#Recrée le dictionnaire data uilisé pour l'encodage
def decode(data):
    dataStartPtr, nImages, types, encodeLens = decodeEntete(data)
    imgs = [dict()]*nImages
    for i in range(nImages):#i représente aussi le size de l'image (toujours dans le même sens)
        #isole les données de l'image
        imgs[i]["encoded"] = data[dataStartPtr:dataStartPtr+encodeLens[i]]
        dataStartPtr+=encodeLens[i]
        #asspcie le bon type de décodage
        if types[i] == 0:
            imgs[i]["encodage"] = "rlc"
            imgs[i]["image"] = rlc.decode(data, i)
        elif types[i] == 1:
            imgs[i]["encodage"] = "huffman"
            imgs[i]["image"] = huffman.decode(data, i)
        elif types[i] == 2:
            imgs[i]["encodage"] = "arithmetique"
            imgs[i]["image"] = arithmetique.decode(data, i)
        else:
            raise("type d'encodage non supporté")
    
    return imgs

def decodeEntete(data):
    ptr = 0
    nImages = int(data[0:7], 2)
    ptr+=8
    types = []
    encodeLens = []
    for i in range(nImages):
        types.append(int(data[ptr:ptr+2],2))#2 bit type
        ptr+=2
        encodeLens.append(int(data[ptr:ptr+24],2))# 24 bit longeur data
        ptr+=24
    return ptr, nImages, types, encodeLens


# compare les statistique des images sources avec 
def calculDebitBinaire(data):
    #TODO faire le calcul du débit binaire
    pass

# compare une image source avec sa version décodé
# retourne vrai si elle sont identique (ce qu'on veut avec lossless comp)
def verificationCodage(srcImg, decImg):    
    for i in range(len(srcImg)):
        if ((srcImg[i]["image"] != decImg[i]["image"]).all()):#TODO revérifier la comparaison après avoir fini les décodage 
            return False
    return True


if __name__ == "__main__":
    #1. lecture des images
    print("Lecture des images")
    img0 = lectureFichier("source0.jpg", "img")
    img1 = lectureFichier("source1.jpg", "img")
    img2 = lectureFichier("source2.jpg", "img")
    img3 = lectureFichier("source3.jpg", "img")
    imgs = [{"image":img0}, {"image":img1}, {"image":img2}, {"image":img3}]

    print("Analyse stat et calcul d'entropie")
    for img in imgs:
        #2. analyse statistiques
        img["statistiques"] = analyseStatistiqueImage(img["image"])        
        #3. calculs d'entropie
        img["entropie"] = calculeEntropie(img["statistiques"])
        
    #4. encodage avec les 3 méthodes
    #le champs encode de chaque image doit contenir la binary string des données avec les métadonnée prêtes à écrire 
    #4.1 huffman
    print("Encodage huffman")
    imgsHuff = copy.deepcopy(imgs)
    for img in imgsHuff:
        img["encode"] = encode("huffman",img)
    #4.2 RLC
    print("Encodage RLC")
    imgsRLC = copy.deepcopy(imgs)
    for img in imgsRLC:
        img["encode"] = encode("rlc",img)
    #4.3 arithmétique
    print("Encodage arithmétique")
    imgsArith = copy.deepcopy(imgs)
    for img in imgsArith:
        img["encode"] = encode("arithmetique",img)
    
    #5. enregistrement des données d'encodage
    print("Enregistrement des données encodées")
    #5.1 huffman
    binStringHuff = genereBinString(imgsHuff)
    enregistreFichier(binStringHuff, "output\\huffmanEncoded.txt")    
    #5.2 RLC
    binStringRLC = genereBinString(imgsRLC)
    enregistreFichier(binStringRLC, "output\\rlcEncoded.txt")    
    #5.3 arithmétique
    binStringArith = genereBinString(imgsArith)
    enregistreFichier(binStringArith, "output\\arithmetiqueEncoded.txt")  

    print("Lecture des données encodées")
    #6. lecture des fichiers encodé (nécessaire pour démontrer la séparation entre l'encodeur et le décodeur)
    imgsEncodeHuff = lectureFichier( "output\\huffmanEncoded.txt", "txt")
    imgsEncodeRLC = lectureFichier("output\\rlcEncoded.txt", "txt")
    imgsEncodeArith = lectureFichier("output\\arithmetiqueEncoded.txt", "txt")

    #7. décodage des images
    #7.1 huffman   
    print("Décodage huffman")
    imgsDecodeHuff = decode(imgsEncodeHuff)
    #7.2 RLC
    print("Décodage RLC")
    imgsDecodeRLC = decode(imgsEncodeRLC)
    #7.3 arithmétique
    print("Décodage arithmétique")
    imgsDecodeArith = decode(imgsEncodeArith)
    
    #8. vérification des images
    print(f"vérification huffman réussi:{verificationCodage(imgs, imgsDecodeHuff)}")
    print(f"vérification RLC réussi:{verificationCodage(imgs, imgsDecodeRLC)}")
    print(f"vérification arithmétique réussi:{verificationCodage(imgs, imgsDecodeArith)}")

    #9. analyses statistiques des encodeurs
    #9.1 huffman
    huffmanDebitBin = calculDebitBinaire(imgsHuff) #total et pour chaque image
    huffmanStats = analyseStatistiqueImage(imgsEncodeHuff)

    #9.2 RLC
    rlcDebitBin = calculDebitBinaire(imgsRLC) #total et pour chaque image
    rlcStats = analyseStatistiqueImage(imgsEncodeRLC)
    
    #9.3 Arithmetique
    arithDebitBin = calculDebitBinaire(imgsArith) #total et pour chaque image
    arithStats = analyseStatistiqueImage(imgsEncodeArith)
    
    #10. TODO print les valeurs intéressantes

    
    print("ligne pour breakpoint")   