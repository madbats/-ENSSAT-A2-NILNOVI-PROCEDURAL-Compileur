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
    pile.append(0)
    base = 0
    ip = 1

    #logger.debug("debutProg, ip = "+ str(ip))


def reserver(n):
    global ip

    #logger.debug("ip before reserver = "+ str(ip))

    if (int(n) > 0):
        i = 0
        while(i < int(n)):
            ip = ip + 1
            pile.append(0)
            i = i + 1

    #logger.debug("ip after reserver = "+ str(ip)+" pile: "+str(pile))

def empiler(val):
    global ip
    global pile

    #logger.debug("ip before empiler = "+ str(ip))
    pile.append(int(val))
    ip = ip + 1
    #logger.debug("empiler "+val)
    #logger.debug("ip after empiler = "+ str(ip)+" pile: "+str(pile))

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
    logger.debug("ip after affectation= "+ str(ip)+" pile: "+str(pile))

def valeurPile():
    global pile
    global ip

    #logger.debug("ip before valeurPile= "+ str(ip))
    index = int(pile[ip])
    #logger.debug("val index: "+ str(index))
    pile[ip] = int(pile[index])
    #logger.debug("val pile["+ str(index)+"]: "+str(pile[ip]))
    #logger.debug("ip after valeurPile= "+ str(ip)+" pile: "+str(pile))

def get():
    global ip
    global pile

    #logger.debug("ip before get= "+ str(ip))
    print("? ",end='')
    val = input()
    try :
        val = int(val)
        index = pile[ip]
        ip = ip - 1
        pile[index] = val
        pile.pop(ip + 1)
        #logger.debug("Got %d with ip %d and placed in index %d pile is now %s",val,ip,index,str(pile))
    except ValueError:
        print("\033[91mERROR\033[0m: Integer expected \033[91m"+str(val)+"\033[0m given")
        erreur()

    #logger.debug("ip after get= "+ str(ip)+" pile: "+str(pile))

def put():
    global ip
    global pile
    #logger.debug("ip before put= "+ str(ip))
    print("> \033[92m"+str(pile[ip])+ "\033[0m")
    pile.pop(ip)
    ip = ip - 1
    #logger.debug("ip after put= "+ str(ip)+" pile: "+str(pile))

def moins():
    global ip
    global pile

    #logger.debug("ip before moins = "+ str(ip))
    pile[ip] = pile[ip] * (-1)
    #logger.debug("ip after moins = "+ str(ip)+" pile: "+str(pile))

def sous():
    global ip
    global pile

    #ip = ip - 1
    #pile[ip] = pile[ip] - pile[ip + 1]
    #pile.pop(ip+1)

    #logger.debug("ip before sous= "+ str(ip))
    var1 = int(pile[ip - 1])
    var2 = int(pile[ip])
    res = var1 - var2
    logger.debug("calcule "+str(var1)+"-"+str(var2)+"="+str(res))
    pile.pop(ip)
    pile.pop(ip - 1)
    pile.append(int(res))

    ip = ip - 1
    #logger.debug("ip after sous = "+ str(ip)+" pile: "+str(pile))

def add():
    global ip
    global pile

    # ip = ip - 1
    # pile[ip] = pile[ip] + pile[ip + 1]
    # pile.pop(ip+1)

    #logger.debug("ip before add = "+ str(ip))
    var1 = int(pile[ip - 1])
    var2 = int(pile[ip])
    res = var1 + var2
    logger.debug("calcule "+str(var1)+"+"+str(var2)+"="+str(res))
    pile.pop(ip)
    pile.pop(ip - 1)
    pile.append(int(res))

    ip = ip - 1
    #logger.debug("ip after add = "+ str(ip)+" pile: "+str(pile))

def mult():
    global ip
    global pile

    # ip = ip - 1
    # pile[ip] = pile[ip] * pile[ip + 1]
    # pile.pop(ip+1)

    #logger.debug("ip before mult = "+ str(ip))
    var1 = int(pile[ip - 1])
    var2 = int(pile[ip])
    res = var1 * var2
    logger.debug("calcule "+str(var1)+"*"+str(var2)+"="+str(res))
    pile.pop(ip)
    pile.pop(ip - 1)
    pile.append(int(res))

    ip = ip - 1
    #logger.debug("ip after mult = "+ str(ip)+" pile: "+str(pile))

def div():
    global ip
    global pile
    
    #logger.debug("ip before div= "+ str(ip))
    var1 = pile[ip - 1]
    var2 = pile[ip]

    if var2 != 0:
        res = var1 / var2
        logger.debug("calcule "+str(var1)+"/"+str(var2)+"="+str(res))
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(int(res))
        #logger.debug("ip after div = "+ str(ip)+" pile: "+str(pile))
    else:
        print("\033[91mERROR\033[0m: Dividing \033[91m%d by 0\033[0m")
        erreur()

    ip = ip - 1
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
    #logger.debug("ip after egal= "+ str(ip)+" pile: "+str(pile))

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
    #logger.debug("ip after diff= "+ str(ip)+" pile: "+str(pile))

def inf():
    global ip
    global pile
    
    if (pile[ip-1] < pile[ip]):
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(1)
    else:
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(0)

    ip = ip - 1
    #logger.debug("ip after inf= "+ str(ip)+" pile: "+str(pile))

def infeg():
    global ip
    global pile
    
    if (pile[ip - 1]<= pile[ip] ):
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(1)
        #logger.debug("True")
    else:
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(0)
        #logger.debug("False")

    ip = ip - 1
    #logger.debug("ip after infeg= "+ str(ip)+" pile: "+str(pile))

def sup():
    global ip
    global pile
    
    if (pile[ip - 1]>pile[ip]):
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(1)
    else:
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(0)

    ip = ip - 1
    #logger.debug("ip after sup= "+ str(ip)+" pile: "+str(pile))

def supeg():
    global ip
    global pile
    
    if (pile[ip - 1] >= pile[ip]):
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(1)
    else:
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(0)

    ip = ip - 1
    #logger.debug("ip after supeg= "+ str(ip)+" pile: "+str(pile))

def et():
    global ip
    global pile
    
    if (pile[ip - 1] and pile[ip]):
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(1)
    else:
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(0)

    ip = ip - 1
    #logger.debug("ip after et= "+ str(ip)+" pile: "+str(pile))

def ou():
    global ip
    global pile
    
    if (pile[ip - 1] or pile[ip ]):
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(1)
    else:
        pile.pop(ip)
        pile.pop(ip - 1)
        pile.append(0)

    ip = ip - 1
    #logger.debug("ip after ou= "+ str(ip)+" pile: "+str(pile))

def non():    
    global ip
    global pile
    
    if (pile[ip] == 0):
        pile.pop(ip)
        pile.append(1)
    else:
        pile.pop(ip)
        pile.append(0)

    #logger.debug("ip after non= "+ str(ip)+" pile: "+str(pile))

def tra(ad):
    global co

    logger.debug("co before tra= " + str(co))
    co = int(ad) - 2
    logger.debug("ip after tra= "+ str(ip)+" pile: "+str(pile))
    logger.debug("co after tra= " + str(co))

def tze(ad):
    global ip
    global pile
    global co

    if (pile[ip] == 0):
        co = int(ad) -2

    ip = ip - 1
    pile.pop(ip + 1)
    logger.debug("ip after tze= "+ str(ip)+" pile: "+str(pile))


def empilerAd(ad):
    global pile
    global ip
    global base

    logger.debug("ip before empilerAd = " + str(ip))
    pile.append(base + 2 + int(ad))
    ip = ip + 1

    logger.debug("empilerAd " + str(base + 2 + int(ad)))
    logger.debug("ip after empilerAd = "+ str(ip)+" pile: "+str(pile))

def reserverBloc():
    global ip
    global pile
    global base

    logger.debug("ip before reserverBloc = " + str(ip))
    pile.append(base)
    pile.append(0)
    ip = ip + 2
    logger.debug("ip after reserverBloc = " + str(ip) + " pile: "+str(pile))

def traStat(a, nbp):
    global ip
    global pile
    global base
    global co

    logger.debug("ip before traStat = " + str(ip))
    logger.debug("base before traStat = " + str(base))
    base = ip - int(nbp) - 1
    pile[base + 1] = co + 1
    co = int(a) - 2
    logger.debug("ip after traStat = " + str(ip) +  " pile: "+str(pile))
    logger.debug("base after traStat = " + str(base))

def retourFonct():
    global ip
    global pile
    global base
    global co

    logger.debug("ip before retourFonct = " + str(ip))
    co = pile[base + 1] - 1
    valRetour = pile[ip]

    while (ip > base):
        pile.pop(ip)
        ip = ip - 1

    base = pile[base]
    pile.pop(ip)
    pile.append(valRetour)
    logger.debug("valRetour = " + str(valRetour))
    logger.debug("ip after retourFonct = " + str(ip) +  " pile: "+str(pile))
    logger.debug("co after retourFonct = " + str(co))

def retourProc():
    global ip
    global pile
    global base
    global co

    logger.debug("ip before retourProc = " + str(ip))
    co = pile[base + 1]

    while (ip > base):
        pile.pop(ip)
        ip = ip - 1

    base = pile[base]
    pile.pop(ip)
    ip = ip - 1
    logger.debug("ip after retourProc = " + str(ip) +  " pile: "+str(pile))

def empilerParam(ad):
    global ip
    global pile
    global base

    logger.debug("ip before empilerParam = " + str(ip))
    pile.append(pile[base + 1 + int(ad)])
    ip = ip + 1
    logger.debug("ip after empilerParam = " + str(ip) +  " pile: "+str(pile))

def erreur():
    #logger.debug("Erreur")

    exit(-1)

def finProg():
    global stack

    stack.close()
    
    exit(0)

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
    i=0
    for line in file:
        logger.debug("%d\t"+line.split(")")[0]+")",i)
        stack.append(line.split(")")[0]+")")
        i+=1
    
    while co < len(stack) - 1:
        s = stack[co]
        func = s.split("(")[0]
        param = (s.split("(")[1]).split(")")[0]
        
        logger.debug("\033[93mip: \033[93m%s\033[0m - \033[94m%s\033[0m",str(ip),str(pile))
        logger.debug("\033[95mco: %d\033[0m - \033[96m"+s+"\033[0m",co)
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
            case "empilerAd":
                empilerAd(param)
            case "reserverBloc":
                reserverBloc()
            case "traStat":
                a = param.split(",")[0]
                nbp = param.split(",")[1]
                traStat(a, nbp)
            case "retourFonct":
                retourFonct()
            case "retourProc":
                retourProc()
            case "empilerParam":
                empilerParam(param)
            case "finProg":
                finProg()
            case _:
                erreur()
                break
        co = co+1;


if __name__ == "__main__":
    main()
