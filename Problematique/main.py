###
# Auteur(s)   : Simon Janelle-Bombardier et William Parent
# Date        : 2026-11-13
# Description : Comparaison de 3 méthode d'encodage entropique. RLC vs Arithmétique vs Huffman
###

# lis un fichier dans le dossier de ressources du nom <nomFichier> et renvoie l'objet File
def lectureFichier(nomFichier):#ajouter arg type pour fichier txt vs image?
    pass

# enregistre les données dans un fichier du nom donné
def enregistreFichier(data, nomFichier):
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
    pass

#retourne un tableau de données 
def decode(methode, data):
    pass

# compare les statistique des images sources avec 
def calculDebitBinaire(srcStats, encStats):
    pass

# compare une image source avec sa version décodé
# retourne vrai si elle sont identique (ce qu'on veut avec lossless comp)
def verificationEncode(srcImg, decImg):
    pass

if __name__ == "__main__":
    print("hello world")


