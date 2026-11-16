from sizeStd import *
import heapq 
import numpy as np

class huffNoeud:
    def __init__(self, symbole=None, occurence=None):
        self.symbole = symbole
        self.occurence = occurence
        self.gauche = None
        self.droite = None

    #permet à heapq de bien trier les noeud
    def __lt__(self, autreNoeud):
        return self.occurence < autreNoeud.occurence
    

def construireArbreHuff(symboles, occurences):
    #crée une heapq des symboles avec leurs occurences
    huffHeapq = [huffNoeud(symb, oc) for symb, oc in zip(symboles, occurences)]
    heapq.heapify(huffHeapq)

    while( len(huffHeapq)>1):
        #retire les deux plus petite propabilité
        enfant_gauche = heapq.heappop(huffHeapq)
        enfant_droit = heapq.heappop(huffHeapq)
        #crée le noeud parent et combine les occurence des 2 petit noeud
        combinoeud = huffNoeud(occurence=enfant_gauche.occurence+enfant_droit.occurence)
        combinoeud.gauche = enfant_gauche
        combinoeud.droite = enfant_droit
        #met le noeud combiné dans la heap
        heapq.heappush(huffHeapq, combinoeud)

    return huffHeapq[0]

def genereTableCode(huffmanNoeud, code="", codeDict=None):
    #crée dictionnaire de cod et code de départ
    if codeDict is None:
        codeDict = {}

    if huffmanNoeud is not None:
        if huffmanNoeud.symbole is not None:
            codeDict[str(int(huffmanNoeud.symbole))] = code
        genereTableCode(huffmanNoeud.gauche, code + "0", codeDict)
        genereTableCode(huffmanNoeud.droite, code + "1", codeDict)
    
    return codeDict 

#génère l'entête encodé
# format : [nSymbole:8bit, symbole1Value:8bit, symbole1Occurence:16bit, symbole2...]
def genereEntete(symboles, occurences):
    nSymb = len(symboles)
    binString = format(nSymb, "08b")#pixel value range 0-255
    for i in range(nSymb):
        binString += format(symboles[i], "08b")# pixel value range 0-255
        binString += format(occurences[i], "016b")#256*256 si tout les pixels ont la même valeur
    print(f"HUFFMAN Grandeur d'entête {len(binString)} bits")
    return binString

#génère la binary string de l'image encodé
def genereEncodage(data, tableCoding):
    binString=""
    for pixel in data:
        binString += tableCoding[str(int(pixel))]
    return binString


def encode(data):
    #1.générer l'arbre de huffman avec tout les symboles
    arbreHuffman = construireArbreHuff(data["statistiques"]["symboles"][0], data["statistiques"]["symboles"][1])
    #2 générer la table d'encodage
    tableCoding = genereTableCode(arbreHuffman)
    #3 générer l'entête encodé
    binString = genereEntete(data["statistiques"]["symboles"][0], data["statistiques"]["symboles"][1])
    #4 encoder l'image
    data1d = data["image"].reshape(-1)
    binString += genereEncodage(data1d, tableCoding)

    return binString


def decodeEntete(data):
    nSymbole = int(data[0:8], 2)
    symboles = []
    occurences = []
    ptr = 8
    for i in range(nSymbole):
        symboles.append(int(data[ptr:ptr+8],2))
        ptr+=8
        occurences.append(int(data[ptr:ptr+16],2))
        ptr+=16
    
    return symboles, occurences, ptr


def decodeData(data, dataPtr, tableEncodage):
    reverseTableEncodage = {v: k for k, v in tableEncodage.items()}
    buff =""
    dataDec=[]
    while dataPtr < len(data):
        buff += data[dataPtr]
        dataPtr+=1

        if buff in reverseTableEncodage.keys():
            dataDec.append(int(reverseTableEncodage[buff]))
            buff = ""
    
    return dataDec
            



def decode(data, size_id):
    #1 decode entete
    symboles, occurences, dataPtr = decodeEntete(data)
    
    #2 génère arbre huffman
    arbreHuffman = construireArbreHuff(symboles, occurences) 

    #3 génère table de code
    tableCode = genereTableCode(arbreHuffman)

    #4 décodage des pixels
    data1d = decodeData(data, dataPtr, tableCode)

    #5 resize image
    size = image_sizes[size_id]
    image = np.asarray(data1d).reshape(size[0], size[1])

    return image