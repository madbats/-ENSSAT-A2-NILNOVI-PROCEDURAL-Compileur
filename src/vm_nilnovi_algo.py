import argparse
import sys
import logging

### Version de Python nécessaire: Python 3.10


logger = logging.getLogger('vm')
####### Déclarations des variables
pile = None
base = None
ip = None

stack = []
co = 0

####### Définition des fonctions

def debutProg():
    global pile
    global base
    global ip

    pile = []
    pile.append(0)
    base = 0
    ip = 0

    logger.debug("debutProg, ip = "+ str(ip))


def reserver(n):
    global ip

    logger.debug("ip before reserver = "+ str(ip))

    if (int(n) > 0):
        i = 0
        while(i < int(n)):
            ip = ip + 1
            pile.append(0)
            i = i + 1

    logger.debug("ip after reserver = "+ str(ip))

def empiler(val):
    global ip
    global pile

    logger.debug("ip before empiler = "+ str(ip))
    pile.append(int(val))
    ip = ip + 1
    logger.debug("empiler"+val)
    logger.debug("ip after empiler = "+ str(ip))

def affectation():
    global pile
    global ip

    logger.debug("ip before affectation = "+ str(ip))
    index = int(pile[ip-1])
    logger.debug("val index: "+ str(index))
    pile[index] = int(pile[ip])
    logger.debug("val pile["+ str(index)+"]: "+ str(pile[index]))
    pile.pop(ip)
    pile.pop(ip-1)
    ip = ip - 2
    logger.debug("ip after affectation= "+ str(ip))

def valeurPile():
    global pile
    global ip

    logger.debug("ip before valeurPile= "+ str(ip))
    index = int(pile[ip])
    logger.debug("val index: "+ str(index))
    pile[ip] = int(pile[index])
    logger.debug("val pile["+ str(index)+"]: "+str(pile[ip]))
    logger.debug("ip after valeurPile= "+ str(ip))

def get():
    global ip
    global pile

    logger.debug("ip before get= "+ str(ip))
    val = input()
    if(isinstance(val, int)):
        index = pile[ip]
        ip = ip - 1
        pile[index] = val
        pile.pop(ip + 1)

    logger.debug("ip after get= "+ str(ip))

def put():
    global ip
    global pile

    logger.debug("ip before put= "+ str(ip))
    logger.debug('\033[92m'+pile[ip]+ '\033[0m')
    ip = ip - 1
    logger.debug("ip after put= "+ str(ip))

def moins():
    global ip
    global pile

    logger.debug("ip before moins = "+ str(ip))
    pile[ip] = pile[ip] * (-1)
    logger.debug("ip after moins = "+ str(ip))

def sous():
    global ip
    global pile

    #ip = ip - 1
    #pile[ip] = pile[ip] - pile[ip + 1]
    #pile.pop(ip+1)

    logger.debug("ip before sous= "+ str(ip))
    var1 = int(pile[ip - 1])
    var2 = int(pile[ip])
    res = var1 - var2
    logger.debug(int(var1)+"-"+int(var2)+"="+int(res))
    pile.pop(ip)
    pile.pop(ip - 1)
    pile.append(int(res))

    ip = ip - 1
    logger.debug("ip after sous = "+ str(ip))

def add():
    global ip
    global pile

    # ip = ip - 1
    # pile[ip] = pile[ip] + pile[ip + 1]
    # pile.pop(ip+1)

    logger.debug("ip before add = "+ str(ip))
    var1 = int(pile[ip - 1])
    var2 = int(pile[ip])
    res = var1 + var2
    logger.debug(int(var1)+"+"+int(var2)+"="+int(res))
    pile.pop(ip)
    pile.pop(ip - 1)
    pile.append(int(res))

    ip = ip - 1
    logger.debug("ip after add = "+ str(ip))

def mult():
    global ip
    global pile

    # ip = ip - 1
    # pile[ip] = pile[ip] * pile[ip + 1]
    # pile.pop(ip+1)

    logger.debug("ip before mult = "+ str(ip))
    var1 = int(pile[ip - 1])
    var2 = int(pile[ip])
    res = var1 * var2
    logger.debug(int(var1)+"*"+int(var2)+"="+int(res))
    pile.pop(ip)
    pile.pop(ip - 1)
    pile.append(int(res))

    ip = ip - 1
    logger.debug("ip after mult = "+ str(ip))

def div():
    global ip
    global pile
    
    logger.debug("ip before div= "+ str(ip))
    var1 = pile[ip - 1]
    var2 = pile[ip]

    if var2 != 0:
        res = var1 / var2
        logger.debug(int(var1)+"/"+int(var2)+"="+int(res))
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(int(res))
        logger.debug("ip after div = "+ str(ip))
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
    logger.debug("Erreur")

    return -1

def finProg():
    global stack

    stack.close()
    
    return 0

####### Programme principal
def main():
    global co,stack,pile,ip,base
    parser = argparse.ArgumentParser(
            description='VM of a NNP program.')
    parser.add_argument('inputfile', type=str, nargs=1,
                            help='name of the input source file')
    parser.add_argument('-d', '--debug', action='store_const', const=logging.DEBUG,
                        default=logging.INFO, help='show debugging info on output')
    args = parser.parse_args()


    filename = sys.argv[1]
    file = open(filename,"r")

    # create logger
    LOGGING_LEVEL = args.debug
    logger.setLevel(LOGGING_LEVEL)
    ch = logging.StreamHandler()
    ch.setLevel(LOGGING_LEVEL)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

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
        co = co+1;


if __name__ == "__main__":
    main()
