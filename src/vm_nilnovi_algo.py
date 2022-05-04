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
    base = 0
    ip = 0


def reserver(n):
    global ip

    if (n > 0):
        ip = ip + n

def empiler(val):
    global ip
    global pile

    ip = ip + 1
    pile.append(val)

def affectation():
    global pile
    global ip

    index = pile[ip-1]
    pile[index] = pile[ip]
    ip = ip - 2
    pile.pop(ip+1)
    pile.pop(ip+2)

def valeurPile():
    global pile
    global ip

    index = pile[ip]
    pile[ip] = pile[index]

def get():
    global ip
    global pile

    val = input()
    if(isinstance(val, int)):
        index = pile[ip]
        ip = ip - 1
        pile[index] = val
        pile.pop(ip + 1)

def put():
    global ip
    global pile

    print(pile[ip])
    ip = ip - 1

def moins():
    global ip
    global pile

    pile[ip] = pile[ip] * (-1)

def sous():
    global ip
    global pile

    ip = ip - 1
    pile[ip] = pile[ip] - pile[ip + 1]
    pile.pop(ip+1)

def add():
    global ip
    global pile

    ip = ip - 1
    pile[ip] = pile[ip] + pile[ip + 1]
    pile.pop(ip+1)

def mult():
    global ip
    global pile

    ip = ip - 1
    pile[ip] = pile[ip] * pile[ip + 1]
    pile.pop(ip+1)

def div():
    global ip
    global pile
    
    ip = ip - 1
    if(pile[ip + 1] != 0):
        pile[ip] = pile[ip] / pile[ip + 1]
    pile.pop(ip+1)

def egal():
    global ip
    global pile
    
    ip = ip - 1
    if (pile[ip] == pile[ip + 1]):
        pile[ip] = 1
    else:
        pile[ip] = 0
    pile.pop(ip + 1)

def diff():
    global ip
    global pile
    
    ip = ip - 1
    if (pile[ip] != pile[ip + 1]):
        pile[ip] = 1
    else:
        pile[ip] = 0
    pile.pop(ip + 1)

def inf():
    global ip
    global pile
    
    ip = ip - 1
    if (pile[ip] < pile[ip + 1]):
        pile[ip] = 1
    else:
        pile[ip] = 0
    pile.pop(ip + 1)

def infeg():
    global ip
    global pile
    
    ip = ip - 1
    if (pile[ip] <= pile[ip + 1]):
        pile[ip] = 1
    else:
        pile[ip] = 0
    pile.pop(ip + 1)

def sup():
    global ip
    global pile
    
    ip = ip - 1
    if (pile[ip] > pile[ip + 1]):
        pile[ip] = 1
    else:
        pile[ip] = 0
    pile.pop(ip + 1)

def supeg():
    global ip
    global pile
    
    ip = ip - 1
    if (pile[ip] >= pile[ip + 1]):
        pile[ip] = 1
    else:
        pile[ip] = 0
    pile.pop(ip + 1)

def et():
    global ip
    global pile
    
    ip = ip - 1
    pile[ip] = pile[ip] and pile[ip + 1]
    pile.pop(ip + 1)

def ou():
    global ip
    global pile
    
    ip = ip - 1
    pile[ip] = pile[ip] or pile[ip + 1]
    pile.pop(ip + 1)

def non():
    global ip
    global pile
    
    global ip
    global pile
    
    pile[ip] = not(pile[ip])

def tra(ad):
    global co
    co = ad

def tze(ad):
    global ip
    global pile
    global co

    if (pile[ip] == 0):
        co = ad
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

while co < len(stack):
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