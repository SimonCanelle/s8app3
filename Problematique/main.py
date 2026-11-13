###
# Auteur(s)   : Simon Janelle-Bombardier et William Parent
# Date        : 2026-11-13
# Description : Comparaison de 3 méthode d'encodage entropique. RLC vs Arithmétique vs Huffman
###


import os
import cv2 as cv
import numpy as np
import copy
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
    with open(FP, "w") as f:
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
    pass


# calcule l'entropie d'une série de symbole
def calculeEntropie(statsDict):
    entropie = 0
    for prob in statsDict["symboles"][2]:
        entropie += prob * np.log2(prob)
    entropie *= -1
    return entropie

# encode les données en une binary string (inclu les métadonnées)
# data est un dictionnaire contenant:
#   - image : array de données de l'image
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
def encode(methode, data):
    if methode == "rlc":
        pass
    elif methode == "huffman":
        pass
    elif methode == "arithmetique":
        pass
    else:
        raise("type d'encodage non supporté")

# génère les métadonnées et construit la binary string à enregistrer 
def genereBinString(imgs):
    return "00000000"

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
def calculDebitBinaire(srcImgs, encImgs):
    pass

# compare une image source avec sa version décodé
# retourne vrai si elle sont identique (ce qu'on veut avec lossless comp)
def verificationCodage(srcImg, decImg):
    pass

if __name__ == "__main__":
    #1. lecture des images
    img0 = lectureFichier("source0.jpg", "img")
    img1 = lectureFichier("source1.jpg", "img")
    img2 = lectureFichier("source2.jpg", "img")
    img3 = lectureFichier("source3.jpg", "img")
    imgs = [{"image":img0}, {"image":img1}, {"image":img2}, {"image":img3}]

    for img in imgs:
        #2. analyse statistiques
        img["statistiques"] = analyseStatistiqueImage(img["image"])        
        #3. calculs d'entropie
        img["entropie"] = calculeEntropie(img["statistiques"])
        
    #4. encodage avec les 3 méthodes
    #le champs encode doit contenir la binary string des données avec les métadonnée prêtes à écrire 
    #4.1 huffman
    imgsHuff = copy.deepcopy(imgs)
    for img in imgsHuff:
        img["encode"] = encode("huffman",img)
    #4.2 RLC
    imgsRLC = copy.deepcopy(imgs)
    for img in imgsRLC:
        img["encode"] = encode("rlc",img)
    #4.3 arithmétique
    imgsArith = copy.deepcopy(imgs)
    for img in imgsArith:
        img["encode"] = encode("arithmetique",img)
    
    #5. enregistrement des données d'encodage
    #5.1 huffman
    binStringHuff = genereBinString(imgsHuff)
    enregistreFichier(binStringHuff, "output\\huffmanEncoded.txt")    
    #5.2 RLC
    binStringRLC = genereBinString(imgsRLC)
    enregistreFichier(binStringRLC, "output\\rlcEncoded.txt")    
    #5.3 arithmétique
    binStringArith = genereBinString(imgsArith)
    enregistreFichier(binStringArith, "output\\arithmetiqueEncoded.txt")  

    #6. lecture des fichiers encodé (nécessaire pour démontrer la séparation entre l'encodeur et le décodeur)
    imgsEncodeHuff = lectureFichier( "output\\huffmanEncoded.txt", "txt")
    imgsEncodeRLC = lectureFichier("output\\rlcEncoded.txt", "txt")
    imgsEncodeArith = lectureFichier("output\\arithmetiqueEncoded.txt", "txt")
    
    #7. décodage des images
    #7.1 huffman   
    imgsDecodeHuff = decode("huffman", imgsEncodeHuff)
    #7.2 RLC
    imgsDecodeRLC = decode("huffman", imgsEncodeRLC)
    #7.3 arithmétique
    imgsDecodeArith = decode("huffman", imgsEncodeArith)
    
    #8. vérification des images
    print(f"vérification huffman réussi:{verificationCodage(imgs, imgsDecodeHuff)}")
    print(f"vérification RLC réussi:{verificationCodage(imgs, imgsDecodeHuff)}")
    print(f"vérification arithmétique réussi:{verificationCodage(imgs, imgsDecodeHuff)}")

    #9. analyses statistiques des encodeurs
    #9.1 huffman
    huffmanDebitBin = calculDebitBinaire(imgsHuff) #total et pour chaque image
    huffmanStats = analyseStatistiqueEncode(imgsEncodeHuff)

    #9.2 RLC
    rlcDebitBin = calculDebitBinaire(imgsRLC) #total et pour chaque image
    rlcStats = analyseStatistiqueEncode(imgsEncodeRLC)
    
    #9.3 Arithmetique
    arithDebitBin = calculDebitBinaire(imgsArith) #total et pour chaque image
    arithStats = analyseStatistiqueEncode(imgsEncodeArith)
    
    
    print("ligne pour breakpoint")   