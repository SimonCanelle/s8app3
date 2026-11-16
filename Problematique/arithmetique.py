from sizeStd import *
import numpy as np

def encode(data):
    pixels = data["image"].ravel()
    symboles, occurrences, _ = data["statistiques"]["symboles"]

    # Distribution cumulative (Fx) des 256 niveaux de gris.
    comptes = np.zeros(256, dtype=np.int64)
    comptes[symboles.astype(int)] = occurrences
    Cum_count = np.concatenate(([0], np.cumsum(comptes)))
    Total_count = len(pixels)
    m = int(2 + np.ceil(np.log2(Total_count)))
    masque = (1 << m) - 1
    masque_msb = 1 << (m - 1)

    L = 0
    U = 2**m - 1
    image_codee = ""

    # Encodage arithmétique avec renormalisations E1, E2 et E3.
    bits_en_attente = 0
    for pixel in pixels:
        K = int(pixel)
        L_old = L
        U_old = U
        L = L_old + (U_old - L_old + 1) * Cum_count[K] // Total_count
        U = L_old + (U_old - L_old + 1) * Cum_count[K + 1] // Total_count - 1

        while True:
            msb_L = (L >> (m - 1)) & 1
            msb_U = (U >> (m - 1)) & 1
            second_L = (L >> (m - 2)) & 1
            second_U = (U >> (m - 2)) & 1

            if (msb_L == 0 and msb_U == 0): # E1
                image_codee += "0"
                L = ((L << 1) & masque) | 0
                U = ((U << 1) & masque) | 1
                while (bits_en_attente > 0):
                    image_codee += "1"
                    bits_en_attente = bits_en_attente - 1
            elif (msb_L == 1 and msb_U == 1): # E2
                image_codee += "1"
                L = ((L << 1) & masque) | 0
                U = ((U << 1) & masque) | 1
                while (bits_en_attente > 0):
                    image_codee += "0"
                    bits_en_attente = bits_en_attente - 1
            elif (second_L == 1 and second_U == 0): # E3
                L = (((L << 1) & masque) | 0) ^ masque_msb
                U = (((U << 1) & masque) | 1) ^ masque_msb
                bits_en_attente = bits_en_attente + 1
            else:
                break

    # Tag
    tag_final = format(int(L), f"0{m}b")

    premier_bit = tag_final[0]
    image_codee += premier_bit

    bit_complementaire = "1" if premier_bit == "0" else "0"
    image_codee += bit_complementaire * bits_en_attente

    image_codee += tag_final[1:]

    debit_reel = len(image_codee) / len(pixels)
    return debit_reel, image_codee, Cum_count



def decode(image_codee, Cum_count, size_id):
    hauteur_image, largeur_image = image_sizes[size_id]
    Total_count = hauteur_image * largeur_image
    
    m = int(2 + np.ceil(np.log2(Total_count)))
    masque = (1 << m) - 1
    masque_msb = 1 << (m - 1)

    L = 0
    U = 2**m - 1

    # Lit les m premiers bits dans le registre tag.
    bits = image_codee[:m].ljust(m, "0")
    tag = int(bits, 2)
    position = m

    pixels = []

    for _ in range(Total_count):
        valeur = ((tag - L + 1) * Total_count - 1) // (U - L + 1)

        # Cherche le symbole dont la fréquence cumulée contient valeur.
        niveau = 0
        while valeur >= Cum_count[niveau + 1]:
            niveau += 1

        pixels.append(niveau)

        # Réduit l'intervalle au sous-intervalle de ce niveau de gris.
        L_old = L
        U_old = U
        L = L_old + (U_old - L_old + 1) * Cum_count[niveau] // Total_count
        U = L_old + (U_old - L_old + 1) * Cum_count[niveau + 1] // Total_count - 1

        # Renormalise jusqu'à ce qu'aucune condition E1, E2 ou E3 ne s'applique.
        while True:
            msb_L = (L >> (m - 1)) & 1
            msb_U = (U >> (m - 1)) & 1
            second_L = (L >> (m - 2)) & 1
            second_U = (U >> (m - 2)) & 1

            bit = int(image_codee[position]) if position < len(image_codee) else 0

            if msb_L == msb_U:  # E1 ou E2
                L = ((L << 1) & masque) | 0
                U = ((U << 1) & masque) | 1
                tag = ((tag << 1) & masque) | bit
                position += 1

            elif second_L == 1 and second_U == 0:  # E3
                L = (((L << 1) & masque) | 0) ^ masque_msb
                U = (((U << 1) & masque) | 1) ^ masque_msb
                tag = (((tag << 1) & masque) | bit) ^ masque_msb
                position += 1

            else:
                break

    image_decodee = np.asarray(pixels, dtype=np.uint8).reshape(hauteur_image, largeur_image)

    return image_decodee
