#!/usr/bin/python

from inspect import isfunction


class Symbole():

    def __init__(self, ident, adresse):
        self.adresse = 0
        self.out = False
        self.bool = False
        self.ident = ident
        self.adresse = adresse

    def setBool(self, val):
        self.bool = val

    def setOut(self, val):
        self.out = val

    def isOut(self):
        return self.out

    def isBool(self):
        return self.bool

    def isParam(self):
        return False

    def isInteger(self):
        return not self.isBool() and not self.isProcedure()

    def getAdresse(self):
        return self.adresse

    def getIdent(self):
        return self.ident

    def isOperation(self):
        return False

    def isFunction(self):
        return False and self.isOperation()

    def isProcedure(self):
        return False and self.isOperation()


class Opperation(Symbole):

    def __init__(self, ident, adresse):
        self.ident = ident
        self.adresse = adresse
        self.params = []

    def addParam(self, par):
        self.params.append(par)

    def isOperation(self):
        return True

    def nombreParam(self):
        return len(self.params)


class Function(Opperation):

    def isFunction(self):
        return True

    def setReturnType(self, type):
        self.returnType = type
        if(type == 'boolean'):
            self.bool = True
        elif(type == 'integer'):
            self.bool = False


class Procedure(Opperation):

    def isProcedure(self):
        return True


class Parametre(Symbole):

    def isParam(self):
        return True


class CodeGenerator():

    def __init__(self):
        self.compilationUnits = []
        self.symboleTable = dict()
        self.compilationUnits = []
        self.coDecalage = 0
        self.compteurVariable = 0
        self.listeIdent = []

    def addUnite(self, unite):
        # print(unite.__class__.__name__)
        self.compilationUnits.append(unite)
        if unite.__class__.__name__ == "OperationGenerator":
            self.coDecalage += len(unite.compilationUnits)-1

    def addVariable(self, symbol):
        self.listeIdent.append(Symbole(symbol, self.compteurVariable + 2))
        self.compteurVariable += 1

    def setType(self, isBool=False):
        for sym in self.listeIdent:
            sym.setBool(isBool)
            self.symboleTable[sym.getIdent()] = sym
        self.listeIdent = []

    def addOperation(self, op):
        self.symboleTable[op.getIdent()] = op

    def getSymboleTable(self):
        return self.symboleTable

    def isSymbolTypeBool(self, symbol):
        return self.symboleTable[symbol].isBool()

    def isSymbolTypeOperation(self, symbol):
        return self.symboleTable[symbol].isOperation()

    def isSymbolTypeFunction(self, symbol):
        return self.symboleTable[symbol].isFunction()

    def getCO(self):
        return len(self.compilationUnits) + self.coDecalage

    def get_instruction_at_index(self, index):
        # print(self.compilationUnits[index].__class__.__name__)
        return self.compilationUnits[index].stringify(self.symboleTable)

    def isOperation(self):
        return False


class CompilationUnite():
    def stringify(self, symbols):
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

    def addVariable(self, symbol):
        if self.paramState:
            self.listeIdent.append(Parametre(symbol, self.compteurVariable))
        else:
            self.listeIdent.append(Symbole(symbol, self.compteurVariable))
        self.compteurVariable += 1

    def toggleParamState(self):
        self.paramState = not self.paramState

    def setOperation(self, operation):
        self.addOperation(operation)
        self.parent.addOperation(operation)
        self.operation = operation

    def addParam(self, param):
        self.operation.addParam(param)

    def getCO(self):
        return len(self.compilationUnits)+self.parent.getCO()

    def getParent(self):
        return self.parent

    def setMode(self, isOut=False):
        if self.paramState:
            for sym in self.listeIdent:
                sym.setOut(isOut)

    def setType(self, isBool=False):
        for sym in self.listeIdent:
            sym.setBool(isBool)
            self.symboleTable[sym.getIdent()] = sym
            if self.paramState:
                self.operation.addParam(sym)
        self.listeIdent = []

    def isOperation(self):
        return True

    def stringify(self, symbols):
        # print("------ IDENTIFIER TABLE Operation ------")
        # for symbole in self.getSymboleTable().values():
        #     # print(symbole)
        #     print("'"+str(symbole.getIdent())+"': "+str(symbole.getAdresse()))
        # print("------ END OF IDENTIFIER TABLE ------")
        instrIndex = 0
        string = ""
        while instrIndex < len(self.compilationUnits):
            string += ("%s\n" % str(self.get_instruction_at_index(instrIndex)))
            instrIndex += 1
        string = string.rstrip(string[-1])
        return string


class debutProg(CompilationUnite):

    def __init__(self):
        return

    def stringify(self, symbols):
        return "debutProg()"


class get(CompilationUnite):

    def stringify(self, symbols):
        return "get()"


class put(CompilationUnite):

    def stringify(self, symbols):
        return "put()"


class finProg(CompilationUnite):

    def __init__(self):
        return

    def stringify(self, symbols):
        unite = "finProg()"
        return unite


class reserver(CompilationUnite):

    def __init__(self, n):
        self.params = []
        self.params.append(n)

    def stringify(self, symbols):
        unite = "reserver("
        unite += str(self.params[0])
        unite += ")"
        return unite


class egal(CompilationUnite):

    def stringify(self, symbols):
        return "egal()"


class diff(CompilationUnite):

    def stringify(self, symbols):
        return "diff()"


class inf(CompilationUnite):

    def stringify(self, symbols):
        return "inf()"


class infeg(CompilationUnite):

    def stringify(self, symbols):
        return "infeg()"


class sup(CompilationUnite):

    def stringify(self, symbols):
        return "sup()"


class supeg(CompilationUnite):

    def stringify(self, symbols):
        return "supeg()"


class et(CompilationUnite):

    def stringify(self, symbols):
        return "et()"


class ou(CompilationUnite):

    def stringify(self, symbols):
        return "ou()"


class non(CompilationUnite):

    def stringify(self, symbols):
        return "non()"


class moins(CompilationUnite):

    def stringify(self, symbols):
        return "moins()"


class sous(CompilationUnite):

    def stringify(self, symbols):
        return "sous()"


class add(CompilationUnite):

    def stringify(self, symbols):
        return "add()"


class mult(CompilationUnite):

    def stringify(self, symbols):
        return "mult()"


class div(CompilationUnite):

    def stringify(self, symbols):
        return "div()"

# classes supp pour procédural


class empilerAd(CompilationUnite):

    def __init__(self, n):
        self.params = []
        self.params.append(n)

    def stringify(self, symbols):
        print("--"+self.params[0]+": " +
              str(symbols[self.params[0]].getAdresse()))
        unite = "empilerAd("
        unite += str(symbols[self.params[0]].getAdresse())
        unite += ")"
        return unite


class reserverBloc(CompilationUnite):

    def stringify(self, symbols):
        unite = "reserverBloc()"
        return unite


class traStat(CompilationUnite):

    def __init__(self, a, nbp):
        self.params = []
        self.params.append(a)
        self.params.append(nbp)

    def stringify(self, symbols):
        unite = "traStat("
        unite += str(symbols[self.params[0]].getAdresse())
        unite += ","
        unite += str(self.params[1])
        unite += ")"
        return unite


class retourFonct(CompilationUnite):

    def stringify(self, symbols):
        unite = "retourFonct()"
        return unite


class retourProc(CompilationUnite):

    def stringify(self, symbols):
        unite = "retourProc()"
        return unite


class empilerParam(CompilationUnite):

    def __init__(self, ad):
        self.params = []
        self.params.append(ad)

    def stringify(self, symbols):
        unite = "empilerParam("
        unite += str(symbols[self.params[0]].getAdresse())
        unite += ")"
        return unite


class empiler(CompilationUnite):
    def __init__(self, val, hasSymbol=True):
        self.params = [val]
        self.hasSymbol = hasSymbol

    def stringify(self, symbols):
        unite = "empiler("
        if(self.hasSymbol):
            # print("has: "+str(self.params[0])+"->"+str(symbols[self.params[0]].getAdresse()))
            unite += str(symbols[self.params[0]].getAdresse())
        else:
            # print("no: "+str(self.params[0]))
            # print("->"+str(symbols[self.params[0]].getAdresse()))
            unite += str(self.params[0])
        unite += ")"
        return unite


class affectation(CompilationUnite):

    def stringify(self, symbols):
        unite = "affectation()"
        return unite


class valeurPile(CompilationUnite):

    def stringify(self, symbols):
        unite = "valeurPile("
        # unite +=str(symbols[self.params[0]].getAdresse())
        unite += ")"
        return unite


class tra(CompilationUnite):

    # init pour un saut vers un symbol
    def __init__(self, ad=None):
        if(ad == None):
            self.params = []
            self.hasSymbol = False
        else:
            self.hasSymbol = True
            self.params = [ad]

    def setAd(self, ad):
        self.params = [ad]

    def stringify(self, symbols):
        unite = "tra("
        unite += str(symbols[self.params[0]].getAdresse()
                     ) if (self.hasSymbol) else str(self.params[0])
        unite += ")"

        return unite


class tze(CompilationUnite):

    def __init__(self, ad=None):
        if(ad == None):
            self.params = []
            self.hasSymbol = False
        else:
            self.hasSymbol = True
            self.params = [ad]

    def setAd(self, ad):
        self.params = [ad]

    def stringify(self, symbols):
        unite = "tze("
        unite += str(symbols[self.params[0]].getAdresse()
                     ) if (self.hasSymbol) else str(self.params[0])
        unite += ")"
        return unite


class erreur(CompilationUnite):

    def __init__(self, n):
        self.params = []
        self.params.append(n)

    def stringify(self, symbols):
        unite = "erreur("
        unite += str(symbols[self.params[0]].getAdresse())
        unite += ")"

        return unite
