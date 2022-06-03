#!/usr/bin/python

import primitives

class Symbole():
    """Symbole dans la table des symboles"""

    def __init__(self, ident, adresse):
        """Initialise un symbole avec identifiant et adresse"""
        self.adresse = 0
        self.mode = None
        self.type = None
        self.ident = ident
        self.adresse = adresse
        self.params = []
        self.symboles = []

    def setType(self, type):
        """Declare si le symbole retourne un boolean"""
        self.type = type

    def isBool(self):
        """Retourne True si le symbole retourne un boolean"""
        return self.type == primitives.BOOLEAN

    def isInteger(self):
        """Retourne True si le symbole retourne un integer"""
        return self.type == primitives.INTEGER

    def isParam(self):
        """Retourne True si le symbole est un parametre d'operation"""
        return False

    def isOut(self):
        """Retourne True si le symbole est de sortie"""
        return self.mode == "in out"

    def getAdresse(self):
        """Retourne l'adresse du symbole"""
        return self.adresse

    def getIdent(self):
        """Retourne l'identifiant"""
        return self.ident

    def isOperation(self):
        """Retourne True si le symbole est une operation"""
        return False

    def isFunction(self):
        """Retourne True si le symbole est une fonction"""
        return False

    def isProcedure(self):
        """Retourne True si le symbole est une procedure"""
        return False

class Operation(Symbole):
    """Operation d'une table de symbole"""

    def setSymbols(self,symboles):
        """Declare la table des symboles lier à cette opération"""
        self.symboles = symboles

    def addParam(self, par):
        """Ajoute un symbole parametre à cette opération"""
        self.params.append(par)

    def isOperation(self):
        return True

    def nombreParam(self):
        """Retourne le nombre de parametre"""
        return len(self.params)

class Function(Operation):
    """Function d'une table de symbole"""

    def isFunction(self):
        return True

    def setReturnType(self, type):
        """Declare le type de retour de la fontion"""
        self.setType(type)

class Procedure(Operation):
    """Function d'une table de symbole"""

    def isProcedure(self):
        return True

class Parametre(Symbole):
    """Parametre d'une table de symbole"""

    def isParam(self):
        return True

    def setMode(self, mode):
        """Declare si le symbole est de sortie"""
        self.mode = mode


class CodeGenerator():
    """Générateur de code"""

    def __init__(self):
        self.symboleTable = dict()
        self.compilationUnits = []
        self.coDecalage = 0
        self.compteurVariable = 0
        self.listeIdent = []

    def addUnite(self, unite):
        """Ajoute une unité de compilation a la table des unités de compilation"""
        # si l'unité rajouter est un OperationGenerator alors les le nombre unité de compilation doit être enregistré
        if unite.isOperation():
            self.coDecalage += len(unite.compilationUnits) - 1
        self.compilationUnits.append(unite)
        

    def addVariable(self, ident):
        """Rajoute une variable à la table des symboles entrain d'être déclaré"""
        self.listeIdent.append(Symbole(ident, self.compteurVariable + 2))
        self.compteurVariable += 1

    def setVariableType(self, type):
        """Declare le type des variables qui ont été déclaté et les rajoutes à la table des symboles"""
        for sym in self.listeIdent:
            sym.setType(type)
            self.symboleTable[sym.getIdent()] = sym
        self.listeIdent = []

    def addOperation(self, op):
        """Rajoute une opération à la table des symboles"""
        self.symboleTable[op.getIdent()] = op

    def getSymboleTable(self):
        """Retourne la table des symboles"""
        return self.symboleTable

    def isSymbolTypeBool(self, ident):
        """Retourne True si le symbole lier à l'identifiant est un boolean"""
        return self.symboleTable[ident].isBool()

    def isSymbolTypeInteger(self, ident):
        """Retourne True si le symbole lier à l'identifiant est un integer"""
        return self.symboleTable[ident].isInteger()

    def isSymbolTypeOperation(self, ident):
        """Retourne True si le symbole lier à l'identifiant est une opération"""
        return self.symboleTable[ident].isOperation()

    def isSymbolTypeFunction(self, ident):
        """Retourne True si le symbole lier à l'identifiant est une fonction"""
        return self.symboleTable[ident].isFunction()


    def isSymbolTypeProcedure(self, ident):
        """Retourne True si le symbole lier à l'identifiant est une procedure"""
        return self.symboleTable[ident].isProcedure()


    def getCO(self):
        """Retourne la valeur du conteur ordinale à cette étape"""
        return len(self.compilationUnits) + self.coDecalage

    def get_instruction_at_index(self, index):
        """Retourne le string de unité de compilation à l'index donné"""
        return self.compilationUnits[index].stringify(self.symboleTable)

    def isOperation(self):
        """Retourne True s'il s'agit d'une OperationGenerator"""
        return False

class CompilationUnite():
    """Unité de compilation abstraite"""

    def stringify(self, symbols):
        """Retourne la ligne de code machine lier à l'unité de compilation"""
        return False

    def isOperation(self):
        """Retourne True s'il s'agit d'une Unité de compilation OperationGenerator"""
        return False

class OperationGenerator(CodeGenerator, CompilationUnite):

    def __init__(self, parent):
        self.parent = parent
        self.operation = None
        self.paramState = False
        self.compilationUnits = []
        self.symboleTable = dict()
        self.compilationUnits = []
        self.coDecalage = 0
        self.compteurVariable = 0
        self.listeIdent = []

    def addVariable(self, ident):
        # Si l'on est entrain de déclarer les parametre alors on rajouter un symboles parametre sinon on rajoute un symbole classique
        if self.paramState:
            self.listeIdent.append(Parametre(ident, self.compteurVariable))
        else:
            self.listeIdent.append(Symbole(ident, self.compteurVariable))
        self.compteurVariable += 1

    def toggleParamState(self):
        """Toggle le l'état parametre signal si l'on est dans le cas ou non de la déclaration de parametre"""
        self.paramState = not self.paramState

    def setOperation(self, operation):
        """Déclare le symbole opération lier à ce générateur et l'ajoute a la table des symboles de lopération et de sont parents"""
        self.addOperation(operation)
        self.parent.addOperation(operation)
        self.operation = operation

    def addParam(self, param):
        """Ajoute un symbole parametre l'opération lier à ce générateur"""
        self.operation.addParam(param)

    def getCO(self):
        return len(self.compilationUnits)+self.parent.getCO()

    def getParent(self):
        """Retourne le générateur de code parent"""
        return self.parent

    def setParamMode(self, mode):
        """Déclare de mode des paramètre entrain d'être déclaré"""
        if self.paramState:
            for sym in self.listeIdent:
                sym.setMode(mode)

    def setVariableType(self, type):
        for sym in self.listeIdent:
            sym.setType(type)
            self.symboleTable[sym.getIdent()] = sym
            if self.paramState:
                self.operation.addParam(sym)
        self.listeIdent = []

    def isOperation(self):
        return True

    def stringify(self, symbols):
        instrIndex = 0
        string = ""
        while instrIndex < len(self.compilationUnits):
            string += ("%s\n" % str(self.get_instruction_at_index(instrIndex)))
            instrIndex += 1
        string = string.rstrip(string[-1])
        return string


class debutProg(CompilationUnite):
    """Unité de compilation de debutProg """

    def __init__(self):
        return

    def stringify(self, symbols):
        return "debutProg()"


class get(CompilationUnite):
    """Unité de compilation de get """

    def stringify(self, symbols):
        return "get()"


class put(CompilationUnite):
    """Unité de compilation de put """

    def stringify(self, symbols):
        return "put()"


class finProg(CompilationUnite):
    """Unité de compilation de finProg """

    def __init__(self):
        return

    def stringify(self, symbols):
        return "finProg()"


class reserver(CompilationUnite):
    """Unité de compilation de reserver """

    def __init__(self, n):
        self.n = n

    def stringify(self, symbols):
        unite = "reserver("
        unite += str(self.n)
        unite += ")"
        return unite


class egal(CompilationUnite):
    """Unité de compilation de egal """

    def stringify(self, symbols):
        return "egal()"


class diff(CompilationUnite):
    """Unité de compilation de diff """

    def stringify(self, symbols):
        return "diff()"


class inf(CompilationUnite):
    """Unité de compilation de inf """

    def stringify(self, symbols):
        return "inf()"


class infeg(CompilationUnite):
    """Unité de compilation de infeg """

    def stringify(self, symbols):
        return "infeg()"


class sup(CompilationUnite):
    """Unité de compilation de sup """

    def stringify(self, symbols):
        return "sup()"


class supeg(CompilationUnite):
    """Unité de compilation de supeg """

    def stringify(self, symbols):
        return "supeg()"


class et(CompilationUnite):
    """Unité de compilation de et """

    def stringify(self, symbols):
        return "et()"


class ou(CompilationUnite):
    """Unité de compilation de ou """

    def stringify(self, symbols):
        return "ou()"


class non(CompilationUnite):
    """Unité de compilation de non """

    def stringify(self, symbols):
        return "non()"


class moins(CompilationUnite):
    """Unité de compilation de moins """

    def stringify(self, symbols):
        return "moins()"


class sous(CompilationUnite):
    """Unité de compilation de sous """

    def stringify(self, symbols):
        return "sous()"


class add(CompilationUnite):
    """Unité de compilation de add """

    def stringify(self, symbols):
        return "add()"


class mult(CompilationUnite):
    """Unité de compilation de mult """

    def stringify(self, symbols):
        return "mult()"


class div(CompilationUnite):
    """Unité de compilation de div """

    def stringify(self, symbols):
        return "div()"


class empilerAd(CompilationUnite):
    """Unité de compilation de empilerAd """

    def __init__(self, n):
        self.n = n

    def stringify(self, symbols):
        
        unite = "empilerAd("
        unite += str(symbols[self.n].getAdresse())
        unite += ")"
        return unite


class reserverBloc(CompilationUnite):
    """Unité de compilation de reserverBloc """

    def stringify(self, symbols):
        return "reserverBloc()"


class traStat(CompilationUnite):
    """Unité de compilation de traStat """

    def __init__(self, a, nbp):
        self.a = a
        self.nbp = nbp

    def stringify(self, symbols):
        unite = "traStat("
        unite += str(symbols[self.a].getAdresse())
        unite += ","
        unite += str(self.nbp)
        unite += ")"
        return unite


class retourFonct(CompilationUnite):
    """Unité de compilation de retourFonct """

    def stringify(self, symbols):
        return "retourFonct()"


class retourProc(CompilationUnite):
    """Unité de compilation de retourProc """

    def stringify(self, symbols):
        return "retourProc()"


class empilerParam(CompilationUnite):
    """Unité de compilation de empilerParam """

    def __init__(self, ad):
        self.ad = ad

    def stringify(self, symbols):
        unite = "empilerParam("
        unite += str(symbols[self.ad].getAdresse())
        unite += ")"
        return unite


class empiler(CompilationUnite):
    """Unité de compilation de empiler """

    def __init__(self, val, isSymbole=True):
        self.val = val
        self.isSymbole = isSymbole

    def stringify(self, symbols):
        unite = "empiler("
        if(self.isSymbole):
            unite += str(symbols[self.val].getAdresse())
        else:
            unite += str(self.val)
        unite += ")"
        return unite


class affectation(CompilationUnite):
    """Unité de compilation de affectation """

    def stringify(self, symbols):
        return "affectation()"


class valeurPile(CompilationUnite):
    """Unité de compilation de valeurPile """

    def stringify(self, symbols):
        return "valeurPile()"


class tra(CompilationUnite):
    """Unité de compilation de tra """

    def __init__(self, ad=None):
        if(ad == None):
            self.isSymbole = False
        else:
            self.isSymbole = True
        self.ad = ad

    def setAd(self, ad):
        self.ad = ad

    def stringify(self, symbols):
        unite = "tra("
        unite += str(symbols[self.ad].getAdresse()
                     ) if (self.isSymbole) else str(self.ad)
        unite += ")"
        return unite


class tze(CompilationUnite):
    """Unité de compilation de tze """

    def __init__(self, ad=None):
        if(ad == None):
            self.isSymbole = False
        else:
            self.isSymbole = True
        self.ad = ad

    def setAd(self, ad):
        self.ad = ad

    def stringify(self, symbols):
        unite = "tze("
        unite += str(symbols[self.ad].getAdresse()
                     ) if (self.isSymbole) else str(self.ad)
        unite += ")"
        return unite


class erreur(CompilationUnite):
    """Unité de compilation de erreur """

    def __init__(self, n):
        self.n = n

    def stringify(self, symbols):
        unite = "erreur("
        unite += str(symbols[self.n].getAdresse())
        unite += ")"

        return unite
