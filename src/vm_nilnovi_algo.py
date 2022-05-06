import sys

### Version de Python nécessaire: Python 3.10


####### Déclarations des variables

pile = None
base = None
ip = None

stack = []
co = 0

filename = sys.argv[1]
file = open(filename, "r")

####### Définition des fonctions

def debutProg():
    global pile
    global base
    global ip

    pile = []
    pile.append(0)
    base = 0
    ip = 0

    print("debutProg, ip = ", ip)


def reserver(n):
    global ip

    print("ip before reserver = ", ip)

    if (int(n) > 0):
        i = 0
        while(i < int(n)):
            ip = ip + 1
            pile.append(0)
            i = i + 1

    print("ip after reserver = ", ip)

def empiler(val):
    global ip
    global pile

    print("ip before empiler = ", ip)
    pile.append(val)
    ip = ip + 1
    print("empiler", val)
    print("ip after empiler = ", ip)

def affectation():
    global pile
    global ip

    print("ip before affectation = ", ip)
    index = int(pile[ip-1])
    print("val index: ", index)
    pile[index] = int(pile[ip])
    print("val pile[", index, "]: ", pile[index])
    pile.pop(ip)
    pile.pop(ip-1)
    ip = ip - 2
    print("ip after affectation= ", ip)

def valeurPile():
    global pile
    global ip

    print("ip before valeurPile= ", ip)
    index = int(pile[ip])
    print("val index: ", index)
    pile[ip] = int(pile[index])
    print("val pile[", index, "]: ", pile[ip])
    print("ip after valeurPile= ", ip)

def get():
    global ip
    global pile

    print("ip before get= ", ip)
    val = input()
    if(isinstance(val, int)):
        index = pile[ip]
        ip = ip - 1
        pile[index] = val
        pile.pop(ip + 1)

    print("ip after get= ", ip)

def put():
    global ip
    global pile

    print("ip before put= ", ip)
    print('\033[92m',pile[ip], '\033[0m')
    ip = ip - 1
    print("ip after put= ", ip)

def moins():
    global ip
    global pile

    print("ip before moins = ", ip)
    pile[ip] = pile[ip] * (-1)
    print("ip after moins = ", ip)

def sous():
    global ip
    global pile

    #ip = ip - 1
    #pile[ip] = pile[ip] - pile[ip + 1]
    #pile.pop(ip+1)

    print("ip before sous= ", ip)
    var1 = int(pile[ip - 1])
    var2 = int(pile[ip])
    res = var1 - var2
    print(var1, "-", var2, "=", res)
    pile.pop(ip)
    pile.pop(ip - 1)
    pile.append(res)

    ip = ip - 1
    print("ip after sous = ", ip)

def add():
    global ip
    global pile

    # ip = ip - 1
    # pile[ip] = pile[ip] + pile[ip + 1]
    # pile.pop(ip+1)

    print("ip before add = ", ip)
    var1 = int(pile[ip - 1])
    var2 = int(pile[ip])
    res = var1 + var2
    print(var1, "+", var2, "=", res)
    pile.pop(ip)
    pile.pop(ip - 1)
    pile.append(res)

    ip = ip - 1
    print("ip after add = ", ip)

def mult():
    global ip
    global pile

    # ip = ip - 1
    # pile[ip] = pile[ip] * pile[ip + 1]
    # pile.pop(ip+1)

    print("ip before mult = ", ip)
    var1 = int(pile[ip - 1])
    var2 = int(pile[ip])
    res = var1 * var2
    print(var1, "*", var2, "=", res)
    pile.pop(ip)
    pile.pop(ip - 1)
    pile.append(res)

    ip = ip - 1
    print("ip after mult = ", ip)

def div():
    global ip
    global pile
    
    print("ip before div= ", ip)
    var1 = pile[ip - 1]
    var2 = pile[ip]

    if var2 != 0:
        res = var1 / var2
        print(var1, "/", var2, "=", res)
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(res)
        print("ip after div = ", ip)
    else:
        erreur()

    # ip = ip - 1
    # if(pile[ip + 1] != 0):
    #     pile[ip] = pile[ip] / pile[ip + 1]
    # pile.pop(ip+1)

def egal():
    global ip
    global pile
    
    if (pile[ip] == pile[ip - 1]):
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(1)
    else:
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(0)

    ip = ip - 1

def diff():
    global ip
    global pile
    
    if (pile[ip] != pile[ip - 1]):
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(1)
    else:
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(0)

    ip = ip - 1

def inf():
    global ip
    global pile
    
    if (pile[ip] < pile[ip - 1]):
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(1)
    else:
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(0)

    ip = ip - 1

def infeg():
    global ip
    global pile
    
    if (pile[ip] <= pile[ip - 1]):
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(1)
    else:
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(0)

    ip = ip - 1

def sup():
    global ip
    global pile
    
    if (pile[ip] > pile[ip - 1]):
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(1)
    else:
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(0)

    ip = ip - 1

def supeg():
    global ip
    global pile
    
    if (pile[ip] >= pile[ip - 1]):
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(1)
    else:
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(0)

    ip = ip - 1

def et():
    global ip
    global pile
    
    pile[ip] = pile[ip] and pile[ip - 1]
    ip = ip - 1
    pile.pop(ip)

def ou():
    global ip
    global pile
    
    pile[ip] = pile[ip] or pile[ip - 1]
    ip = ip - 1
    pile.pop(ip)

def non():    
    global ip
    global pile
    
    pile[ip] = not(pile[ip])

def tra(ad):
    global co
    co = int(ad)

def tze(ad):
    global ip
    global pile
    global co

    if (pile[ip] == 0):
        co = int(ad)
    else:
        co = co + 1    
    ip = ip -1
    pile.pop(ip + 1)

def erreur():
    print("Erreur")

    return -1

def finProg():
    global stack

    stack.close()
    
    return 0

####### Programme principal

for line in file:
    stack.append(line)

while co < len(stack) - 1:
    s = stack[co]
    func = s.split("(")[0]
    param = (s.split("(")[1]).split(")")[0]
    
    match func:
        case "debutProg":
            debutProg()
        case "reserver":
            reserver(param)
        case "empiler":
            empiler(param)
        case "affectation":
            affectation()
        case "valeurPile":
            valeurPile()
        case "get":
            get()
        case "put":
            put()
        case "moins":
            moins()
        case "sous":
            sous()
        case "add":
            add()
        case "mult":
            mult()
        case "div":
            div()
        case "egal":
            egal()
        case "diff":
            diff()
        case "inf":
            inf()
        case "infeg":
            infeg()
        case "sup":
            sup()
        case "supeg":
            supeg()
        case "et":
            et()
        case "ou":
            ou()
        case "non":
            non()
        case "tra":
            tra(param)
        case "tze":
            tze(param)
        case "finProg":
            finProg()
        case _:
            erreur()
            break

    co = co +1