import numpy as np

# Initialisations
NomFichierCompresse = "CodageLZ77.bin"
DimBuffer = 10       # À modifier
DimF_Analyse = 10    # À modifier
Buffer = np.zeros(DimBuffer, dtype=np.uint8)

# Lecture du fichier de départ
with open("TexteACompresse.txt", "r") as fichier:
    Texte = fichier.read().splitlines()
Texte = "".join(Texte)
Texte = np.array([ord(caractere) for caractere in Texte], dtype=np.uint8)
LongueurTexteOriginal = len(Texte)

############# COMPRESSEUR LZ77 #############

TexteCodee = []
Position = 0

# Balayage du texte
while Position < LongueurTexteOriginal:

    # Longueur maximale de correspondance possible
    LongueurMax = min(DimF_Analyse - 1, LongueurTexteOriginal - Position - 1)

    MeilleureLongueur = 0
    MeilleurePosition = 0

    # Recherche de la meilleure correspondance dans le buffer
    for j in range(DimBuffer - 1, -1, -1):
        Longueur = 0
        Distance = DimBuffer - j

        while (Longueur < LongueurMax):
            if Longueur < Distance:
                CaractereReference = Buffer[j + Longueur]
            else:
                CaractereReference = Texte[Position + Longueur - Distance]
            if CaractereReference == Texte[Position + Longueur]:
                Longueur += 1
            else:
                break
            
        if Longueur > MeilleureLongueur:
            MeilleureLongueur = Longueur
            MeilleurePosition = j

    # Si une correspondance a été trouvée
    if MeilleureLongueur > 0:
        Distance = DimBuffer - MeilleurePosition
        CaractereSuivant = Texte[Position + MeilleureLongueur]
        TexteCodee.extend([Distance, MeilleureLongueur, CaractereSuivant])
        LongueurConsommee = MeilleureLongueur + 1
    else:
        # Aucune correspondance : codage du caractère seul
        TexteCodee.extend([0, 0, Texte[Position]])
        LongueurConsommee = 1

    Buffer = np.concatenate((Buffer, Texte[Position:Position + LongueurConsommee]))[-DimBuffer:]
    Position += LongueurConsommee


# Conversion du vecteur codé en tableau NumPy
TexteCodee = np.array(TexteCodee, dtype=np.uint8)

# Enregistrement
with open(NomFichierCompresse, "wb") as fichier:
    fichier.write(TexteCodee.tobytes())


############ DECOMPRESSEUR LZ77 ############

# Initialisation du vecteur contenant le texte décodé
TexteDecodee = [0] * DimBuffer

# Vérification du format des codes
if len(TexteCodee) % 3 != 0:
    raise ValueError("Le vecteur compressé doit contenir des codes de 3 octets.")

for i in range(0, len(TexteCodee), 3):
    Code = TexteCodee[i:i+3]
    if Code[1] == 0:
        # Le code contient un seul caractère à décoder
        TexteDecodee.append(int(Code[2]))
    else:
        # Le code contient plus qu'un seul caractère à décoder
        Distance = int(Code[0])
        Longueur = int(Code[1])
        for j in range(Longueur):
            TexteDecodee.append(TexteDecodee[-Distance])
        TexteDecodee.append(int(Code[2]))

# Suppression du buffer initial
TexteDecodee = np.array(TexteDecodee[DimBuffer:], dtype=np.uint8)

# Enregistrement
with open("TexteDecompresse.txt", "wb") as fichier:
    fichier.write(TexteDecodee.tobytes())


# Vérification des données
if np.array_equal(TexteDecodee, Texte):
    print("Décompression réussie : le texte original a été reconstruit.")
else:
    print("ERREUR : le texte décompressé diffère du texte original.")

if __name__ == "__main__":
    print("hello world")