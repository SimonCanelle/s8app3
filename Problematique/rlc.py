from sizeStd import *
import numpy as np

rlcCounterMax = 4

def encode(data):
    #data is a 2d array of the image 
    #1. applatir l'array
    data1d = data["image"].reshape(-1)
    #2. faire le compte des symbole en tuples
    comptes = countRepetition(data1d)
    #3. encoder les paires en string binaire
    binstring = encodePairs(comptes)
    print(f"len bitstring {len(binstring)}")
    return binstring

#TODO la logique peut clairement être opimisée
def countRepetition(data1d):
    counter = 0  
    datasize = len(data1d)  
    lastVal = -1
    countTupList = []
    for i,pix in enumerate(data1d):
        if pix == lastVal:
            counter += 1
            if counter == rlcCounterMax:
                countTupList.append(tuple((pix, counter)))
                if i + 1 == datasize:#fix pour pas print 2x 
                    break
                counter = 0            
        else :
            if lastVal != -1 and counter > 0: #fix for first loop and maxcounts
                countTupList.append(tuple((lastVal, counter)))
            counter = 1

        if i + 1 == datasize:#last value fix
            countTupList.append(tuple((pix, counter)))
        
        lastVal = pix
    
    return countTupList

def encodePairs(tupleList):
    binstr = ""
    #closest n bit that can contain this counter
    nBitCounter = np.ceil(np.log2(rlcCounterMax))
    #itere au travers des tuples pour les encoder en bin string
    for tup in tupleList:
        charBin = format(tup[0], "08b")
        countBin = format(tup[1]-1, f"0{int(nBitCounter)}b")

        binstr +=  charBin + countBin
        
    return binstr


def decode(data, size_id):
    #1 reconstruire les données
    dataPtr = 0
    data1d = []
    nBitCounter = int(np.ceil(np.log2(rlcCounterMax)))
    while dataPtr < len(data):
        pixValue = int(data[dataPtr:dataPtr+8],2)
        dataPtr+=8
        repCount = int(data[dataPtr:dataPtr+nBitCounter],2)+1
        dataPtr+=nBitCounter

        for i in range(repCount):
            data1d.append(pixValue)

    #2 resize properly
    size = image_sizes[size_id]
    image = np.asarray(data1d).reshape(size[0], size[1])

    return image

