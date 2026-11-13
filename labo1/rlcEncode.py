def countRepetition(charArray):
    counter = 0
    counterMax = 4
    lastChar = ""
    countTupList = []
    for char in charArray:
        if char == lastChar:
            counter += 1
            if counter == counterMax:
                countTupList.append(tuple((char, counter)))
                counter = 0            
        else :
            if lastChar != "" and counter > 0: #fix for first loop and 6 counts
                countTupList.append(tuple((lastChar, counter)))
            counter = 1
        lastChar = char
    return countTupList

def encodePairs(tupleList):
    binstr = ""
    for tup in tupleList:
        charValue = ord(tup[0])-ord("A")
        countValue = tup[1] - 1

        charBin = format(charValue, "05b")
        countBin = format(countValue, "03b")

        binstr +=  charBin + countBin
        
    return binstr

input_file = "AAAAAAABBBBCCCDDDDDDDDDDEEEEEAAAAADDDDCCCCCCCCEEEEEEEEEEEAAAAAABBBBEEDDDDAAAAACCCCCCCCCCC"

if __name__ == "__main__":
    a = countRepetition(input_file)
    b = encodePairs(a)
    with open("labo1/encoded.txt", "w+", encoding='utf-8') as f:
        f.write(b)
    

    


