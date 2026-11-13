
def densityCumul(Tableau):
    cumul = 0
    for i in range(1,len(Tableau)):
        Tableau[i][2] = Tableau[i][1] + Tableau[i-1][2]    
    return Tableau


input_string = "UUCTCU"
Tableau = [["0",0,0], ["U", 0.2, 0], ["T", 0.3, 0], ["C", 0.5, 0]]

Tableau = densityCumul(Tableau)
print(Tableau)

l = 0
u = 1

for car in input_string:
    if car == "U":
        i = 1
    elif car == "T":
        i = 2
    elif car == "C":
        i = 3 
    ltemp = l
    utemp = u
    l = ltemp + (utemp-ltemp) * Tableau[i-1][2]
    u = ltemp + (utemp-ltemp) * Tableau[i][2]
    print(f"car:{car} l:{l} u:{u}")

tag = (l+u)/2
print(tag)

bin = format(int(round(tag * 10000)), "09b")
print(bin)




    