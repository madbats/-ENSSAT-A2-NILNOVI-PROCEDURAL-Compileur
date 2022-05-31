#!/usr/bin/python

# @package anasyn
# 	Syntactical Analyser package.
#

from copy import copy
import sys
import argparse
import re
import logging

import analex
from codeGenerator import *

logger = logging.getLogger('anasyn')
codeGenerator = CodeGenerator()
operationGenerator = None
DEBUG = False
LOGGING_LEVEL = logging.DEBUG


class AnaSynException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

########################################################################
# Syntactical Diagrams
########################################################################


def program(lexical_analyser):
    global codeGenerator
    specifProgPrinc(lexical_analyser)
    lexical_analyser.acceptKeyword("is")
    corpsProgPrinc(lexical_analyser)


def specifProgPrinc(lexical_analyser):
    global codeGenerator
    lexical_analyser.acceptKeyword("procedure")
    
    ident = lexical_analyser.acceptIdentifier()
    logger.debug("Name of program : "+ident)


def corpsProgPrinc(lexical_analyser):
    global codeGenerator
    codeGenerator.addUnite(debutProg())
    if not lexical_analyser.isKeyword("begin"):
        logger.debug("Parsing declarations")
        
        
        partieDecla(lexical_analyser)
        logger.debug("End of declarations")
    lexical_analyser.acceptKeyword("begin")

    


    if not lexical_analyser.isKeyword("end"):
        logger.debug("Parsing instructions")
        suiteInstr(lexical_analyser)
        logger.debug("End of instructions")

    lexical_analyser.acceptKeyword("end")
    lexical_analyser.acceptFel()
    codeGenerator.addUnite(finProg())
    logger.debug("End of program")


def partieDecla(lexical_analyser):
    global codeGenerator
    if lexical_analyser.isKeyword("procedure") or lexical_analyser.isKeyword("function"):
        tra1 = tra()
        codeGenerator.addUnite(tra1)
        listeDeclaOp(lexical_analyser)
        tra1.setAd(codeGenerator.getCO())
        if not lexical_analyser.isKeyword("begin"):
            listeDeclaVar(lexical_analyser)
    else:
        listeDeclaVar(lexical_analyser)

def listeDeclaOp(lexical_analyser):
    global codeGenerator
    declaOp(lexical_analyser)
    lexical_analyser.acceptCharacter(";")
    if lexical_analyser.isKeyword("procedure") or lexical_analyser.isKeyword("function"):
        listeDeclaOp(lexical_analyser)

def declaOp(lexical_analyser):
    global codeGenerator
    operationGenerator = OperationGenerator(copy(codeGenerator))
    
    codeGenerator = operationGenerator
    if lexical_analyser.isKeyword("procedure"):
        procedure(lexical_analyser)
    if lexical_analyser.isKeyword("function"):
        fonction(lexical_analyser)
    codeGenerator = copy(codeGenerator.getParent())
    
    codeGenerator.addUnite(copy(operationGenerator))
    operationGenerator = None

def procedure(lexical_analyser):
    global codeGenerator
    lexical_analyser.acceptKeyword("procedure")
    ident = lexical_analyser.acceptIdentifier()
    logger.debug("Name of procedure : "+ident)
    proc = Procedure(ident,codeGenerator.getCO())
    codeGenerator.setOperation(proc)
    partieFormelle(lexical_analyser)

    lexical_analyser.acceptKeyword("is")
    corpsProc(lexical_analyser)


def fonction(lexical_analyser):
    global codeGenerator
    lexical_analyser.acceptKeyword("function")
    ident = lexical_analyser.acceptIdentifier()
    logger.debug("Name of function : "+ident)
    func = Function(ident,codeGenerator.getCO())
    codeGenerator.setOperation(func)
    partieFormelle(lexical_analyser)

    lexical_analyser.acceptKeyword("return")
    ret = nnpType(lexical_analyser)
    func.setReturnType(ret)
    lexical_analyser.acceptKeyword("is")
    corpsFonct(lexical_analyser)


def corpsProc(lexical_analyser):
    global codeGenerator
    if not lexical_analyser.isKeyword("begin"):
        partieDeclaProc(lexical_analyser)
    lexical_analyser.acceptKeyword("begin")
    suiteInstr(lexical_analyser)
    lexical_analyser.acceptKeyword("end")


def corpsFonct(lexical_analyser):
    global codeGenerator
    if not lexical_analyser.isKeyword("begin"):
        partieDeclaProc(lexical_analyser)
    lexical_analyser.acceptKeyword("begin")
    suiteInstrNonVide(lexical_analyser)
    lexical_analyser.acceptKeyword("end")


def partieFormelle(lexical_analyser):
    global codeGenerator
    lexical_analyser.acceptCharacter("(")
    codeGenerator.toggleParamState()
    if not lexical_analyser.isCharacter(")"):
        listeSpecifFormelles(lexical_analyser)
    lexical_analyser.acceptCharacter(")")
    codeGenerator.toggleParamState()


def listeSpecifFormelles(lexical_analyser):
    global codeGenerator
    specif(lexical_analyser)
    if not lexical_analyser.isCharacter(")"):
        lexical_analyser.acceptCharacter(";")
        listeSpecifFormelles(lexical_analyser)


def specif(lexical_analyser):
    global codeGenerator
    nb = listeIdent(lexical_analyser)
    lexical_analyser.acceptCharacter(":")
    if lexical_analyser.isKeyword("in"):
        isOut = mode(lexical_analyser)
        codeGenerator.setMode((isOut == 'out'))

    nnpType(lexical_analyser)


def mode(lexical_analyser):
    global codeGenerator
    lexical_analyser.acceptKeyword("in")
    if lexical_analyser.isKeyword("out"):
        lexical_analyser.acceptKeyword("out")
        logger.debug("in out parameter")
        return 'out'
    else:
        logger.debug("in parameter")
        return 'in'


def nnpType(lexical_analyser):
    global codeGenerator
    if lexical_analyser.isKeyword("integer"):
        lexical_analyser.acceptKeyword("integer")
        codeGenerator.setType(False)
        logger.debug("integer type")
        return 'integer'
    elif lexical_analyser.isKeyword("boolean"):
        lexical_analyser.acceptKeyword("boolean")
        codeGenerator.setType(True)
        logger.debug("boolean type")
        return 'bool'
    else:
        logger.error("Unknown type found <" +
                     lexical_analyser.get_value() + ">!")
        raise AnaSynException("Unknown type found <" +
                              lexical_analyser.get_value() + ">!")


def partieDeclaProc(lexical_analyser):
    global codeGenerator
    listeDeclaVar(lexical_analyser)


def listeDeclaVar(lexical_analyser):
    global codeGenerator
    declaVar(lexical_analyser)
    if lexical_analyser.isIdentifier():
        listeDeclaVar(lexical_analyser)

def declaVar(lexical_analyser):
    global codeGenerator
    nb = listeIdent(lexical_analyser)
    lexical_analyser.acceptCharacter(":")
    logger.debug("now parsing type...")    
    codeGenerator.addUnite(reserver(nb))
    nnpType(lexical_analyser)
    lexical_analyser.acceptCharacter(";")


def listeIdent(lexical_analyser):
    global codeGenerator
    ident = lexical_analyser.acceptIdentifier()
    logger.debug("identifier found: "+str(ident))
    codeGenerator.addVariable(ident)

    if lexical_analyser.isCharacter(","):
        lexical_analyser.acceptCharacter(",")
        return listeIdent(lexical_analyser)+1
    return 1

def suiteInstrNonVide(lexical_analyser):
    global codeGenerator
    instr(lexical_analyser)
    if lexical_analyser.isCharacter(";"):
        lexical_analyser.acceptCharacter(";")
        suiteInstrNonVide(lexical_analyser)


def suiteInstr(lexical_analyser):
    global codeGenerator
    if not lexical_analyser.isKeyword("end"):
        suiteInstrNonVide(lexical_analyser)


def instr(lexical_analyser):
    global codeGenerator
    if lexical_analyser.isKeyword("while"):
        boucle(lexical_analyser)
    elif lexical_analyser.isKeyword("if"):
        altern(lexical_analyser)
    elif lexical_analyser.isKeyword("get") or lexical_analyser.isKeyword("put"):
        es(lexical_analyser)
    elif lexical_analyser.isKeyword("return"):
        retour(lexical_analyser)
    elif lexical_analyser.isIdentifier():
        ident = lexical_analyser.acceptIdentifier()
        if lexical_analyser.isSymbol(":="):
            # affectation
            codeGenerator.addUnite(empiler(ident)) ###empiler(ident, true) --> adresse / empiler(ident, false) --> valeur
            lexical_analyser.acceptSymbol(":=")
            type = expression(lexical_analyser)
            if((codeGenerator.isSymbolTypeBool(ident) and type == 'integer') or \
                (not codeGenerator.isSymbolTypeBool(ident) and type != 'integer') ):
                raise AnaSynException("Type mismatch. Did not expected : "+type)
            codeGenerator.addUnite(affectation())
            logger.debug("parsed affectation")
        elif lexical_analyser.isCharacter("("):
            lexical_analyser.acceptCharacter("(")
            if not lexical_analyser.isCharacter(")"):
                listePe(lexical_analyser)

            lexical_analyser.acceptCharacter(")")
            logger.debug("parsed procedure call")
        else:
            logger.error("Expecting procedure call or affectation!")
            raise AnaSynException("Expecting procedure call or affectation!")

    else:
        logger.error("Unknown Instruction <" +
                     lexical_analyser.get_value() + ">!")
        raise AnaSynException("Unknown Instruction <" +
                              lexical_analyser.get_value() + ">!")


def listePe(lexical_analyser):
    global codeGenerator
    expression(lexical_analyser)
    if lexical_analyser.isCharacter(","):
        lexical_analyser.acceptCharacter(",")
        return 1 + listePe(lexical_analyser)
    return 1


def expression(lexical_analyser):
    global codeGenerator
    logger.debug("parsing expression: " + str(lexical_analyser.get_value()))

    type = exp1(lexical_analyser)
    if lexical_analyser.isKeyword("or"):
        lexical_analyser.acceptKeyword("or")
        exp1(lexical_analyser)
        type= 'bool'
        codeGenerator.addUnite(ou())
    return type


def exp1(lexical_analyser):
    global codeGenerator
    logger.debug("parsing exp1")

    type = exp2(lexical_analyser)
    if lexical_analyser.isKeyword("and"):
        lexical_analyser.acceptKeyword("and")
        exp2(lexical_analyser)
        type= 'bool'
        codeGenerator.addUnite(et())
    return type

def exp2(lexical_analyser):
    global codeGenerator
    logger.debug("parsing exp2")
    op = None
    type = exp3(lexical_analyser)
    if lexical_analyser.isSymbol("<") or \
            lexical_analyser.isSymbol("<=") or \
            lexical_analyser.isSymbol(">") or \
            lexical_analyser.isSymbol(">="):
        op = opRel(lexical_analyser)
        exp3(lexical_analyser)
        type = 'bool'
    elif lexical_analyser.isSymbol("=") or \
            lexical_analyser.isSymbol("/="):
        op = opRel(lexical_analyser)
        exp3(lexical_analyser)
        type = 'bool'
    if(not(op == None)) :
        codeGenerator.addUnite(op)
    return type


def opRel(lexical_analyser):
    global codeGenerator
    logger.debug("parsing relationnal operator: " +
                 lexical_analyser.get_value())

    if lexical_analyser.isSymbol("<"):
        lexical_analyser.acceptSymbol("<")
        return inf()
    elif lexical_analyser.isSymbol("<="):
        lexical_analyser.acceptSymbol("<=")
        return infeg()
    elif lexical_analyser.isSymbol(">"):
        lexical_analyser.acceptSymbol(">")
        return sup()
    elif lexical_analyser.isSymbol(">="):
        lexical_analyser.acceptSymbol(">=")
        return supeg()
    elif lexical_analyser.isSymbol("="):
        lexical_analyser.acceptSymbol("=")
        return egal()
    elif lexical_analyser.isSymbol("/="):
        lexical_analyser.acceptSymbol("/=")
        return diff()
    else:
        msg = "Unknown relationnal operator <" + lexical_analyser.get_value() + ">!"
        logger.error(msg)
        raise AnaSynException(msg)


def exp3(lexical_analyser):
    global codeGenerator
    logger.debug("parsing exp3")
    type =exp4(lexical_analyser)

    op = None
    if lexical_analyser.isCharacter("+") or lexical_analyser.isCharacter("-"):
        op = opAdd(lexical_analyser)
        type = 'integer'
        exp4(lexical_analyser)
    if(not(op == None)) :
        codeGenerator.addUnite(op)
    return type

def opAdd(lexical_analyser):
    global codeGenerator
    logger.debug("parsing additive operator: " + lexical_analyser.get_value())
    if lexical_analyser.isCharacter("+"):
        lexical_analyser.acceptCharacter("+")
        return add()
    elif lexical_analyser.isCharacter("-"):
        lexical_analyser.acceptCharacter("-")
        return sous()
    else:
        msg = "Unknown additive operator <" + lexical_analyser.get_value() + ">!"
        logger.error(msg)
        raise AnaSynException(msg)


def exp4(lexical_analyser):
    global codeGenerator
    logger.debug("parsing exp4")
    op = None
    type = prim(lexical_analyser)
    if lexical_analyser.isCharacter("*") or lexical_analyser.isCharacter("/"):
        op = opMult(lexical_analyser)
        type = prim(lexical_analyser)
    if(not(op == None)) :
        codeGenerator.addUnite(op)
    return type


def opMult(lexical_analyser):
    global codeGenerator
    logger.debug("parsing multiplicative operator: " +
                 lexical_analyser.get_value())
    if lexical_analyser.isCharacter("*"):
        lexical_analyser.acceptCharacter("*")
        return mult()
    elif lexical_analyser.isCharacter("/"):
        lexical_analyser.acceptCharacter("/")
        return div()
    else:
        msg = "Unknown multiplicative operator <" + lexical_analyser.get_value() + ">!"
        logger.error(msg)
        raise AnaSynException(msg)


def prim(lexical_analyser):
    global codeGenerator
    logger.debug("parsing prim")
    op = None
    if lexical_analyser.isCharacter("+") or lexical_analyser.isCharacter("-") or lexical_analyser.isKeyword("not"):
        op = opUnaire(lexical_analyser)
    type = elemPrim(lexical_analyser)
    if(not(op == None) ) :
        codeGenerator.addUnite(op)
    return type


def opUnaire(lexical_analyser):
    global codeGenerator
    logger.debug("parsing unary operator: " + lexical_analyser.get_value())
    if lexical_analyser.isCharacter("+"):
        lexical_analyser.acceptCharacter("+")
        return None
    elif lexical_analyser.isCharacter("-"):
        lexical_analyser.acceptCharacter("-")
        return moins()

    elif lexical_analyser.isKeyword("not"):
        lexical_analyser.acceptKeyword("not")
        return non()
    else:
        msg = "Unknown additive operator <" + lexical_analyser.get_value() + ">!"
        logger.error(msg)
        raise AnaSynException(msg)


def elemPrim(lexical_analyser):
    global codeGenerator
    logger.debug("parsing elemPrim: " + str(lexical_analyser.get_value()))
    type = None
    if lexical_analyser.isCharacter("("):
        lexical_analyser.acceptCharacter("(")
        type = expression(lexical_analyser)
        lexical_analyser.acceptCharacter(")")
    elif lexical_analyser.isInteger() or lexical_analyser.isKeyword("true") or lexical_analyser.isKeyword("false"):
        return valeur(lexical_analyser)
    elif lexical_analyser.isIdentifier():
        ident = lexical_analyser.acceptIdentifier()
        if lexical_analyser.isCharacter("("):			# Appel fonct
            lexical_analyser.acceptCharacter("(")
            codeGenerator.addUnite(reserverBloc())
            if not lexical_analyser.isCharacter(")"):
                nbParam = listePe(lexical_analyser)

            lexical_analyser.acceptCharacter(")")
            logger.debug("parsed procedure call")
            codeGenerator.addUnite(tra(ident))
            logger.debug("Call to function: " + ident)
            codeGenerator.addUnite(traStat(ident, nbParam))
        else:
            logger.debug("Use of an identifier as an expression: " + ident)
            codeGenerator.addUnite(empiler(ident))
            codeGenerator.addUnite(valeurPile())
        if(codeGenerator.isSymbolTypeFunction(ident) or not codeGenerator.isSymbolTypeOperation(ident) ):
            if (codeGenerator.isSymbolTypeBool(ident)):
                type = 'bool'
            else:
                type = 'integer'
        else:
            logger.error("Procedures cannot return values")
            raise AnaSynException("Procedures cannot return values!")
    else:
        logger.error("Unknown Value!")
        raise AnaSynException("Unknown Value!")
    return type


def valeur(lexical_analyser):
    global codeGenerator
    if lexical_analyser.isInteger():
        entier = lexical_analyser.acceptInteger()
        logger.debug("integer value: " + str(entier))
        logger.debug("entier:"+str(entier))
        codeGenerator.addUnite(empiler(entier,False))
        return "integer"
    elif lexical_analyser.isKeyword("true") or lexical_analyser.isKeyword("false"):
        vtype = valBool(lexical_analyser)
        return vtype
    else:
        logger.error("Unknown Value! Expecting an integer or a boolean value!")
        raise AnaSynException(
            "Unknown Value ! Expecting an integer or a boolean value!")


def valBool(lexical_analyser):
    global codeGenerator
    if lexical_analyser.isKeyword("true"):
        lexical_analyser.acceptKeyword("true")
        codeGenerator.addUnite(empiler(1,False))
        logger.debug("boolean true value")

    else:
        logger.debug("boolean false value")
        lexical_analyser.acceptKeyword("false")
        codeGenerator.addUnite(empiler(0,False))

    return "boolean"


def es(lexical_analyser):
    global codeGenerator
    logger.debug("parsing E/S instruction: " + lexical_analyser.get_value())
    if lexical_analyser.isKeyword("get"):
        lexical_analyser.acceptKeyword("get")
        lexical_analyser.acceptCharacter("(")
        ident = lexical_analyser.acceptIdentifier()
        lexical_analyser.acceptCharacter(")")
        if(codeGenerator.isSymbolTypeBool(ident)):
            raise AnaSynException("Type mismatch. Did not expected : integer")
        codeGenerator.addUnite(empiler(ident,True))
        codeGenerator.addUnite(get())
        logger.debug("Call to get "+ident)
    elif lexical_analyser.isKeyword("put"):
        
        lexical_analyser.acceptKeyword("put")
        lexical_analyser.acceptCharacter("(")
        type = expression(lexical_analyser)
        if(type !='integer'):
            raise AnaSynException("Type mismatch. Expected : integer got "+ type)
        lexical_analyser.acceptCharacter(")")
        logger.debug("Call to put")
        codeGenerator.addUnite(put())
    else:
        logger.error("Unknown E/S instruction!")
        raise AnaSynException("Unknown E/S instruction!")


def boucle(lexical_analyser):
    global codeGenerator
    logger.debug("parsing while loop: ")
    lexical_analyser.acceptKeyword("while")
    ad1 = codeGenerator.getCO()
    type = expression(lexical_analyser)
    if(type =='integer'):
            raise AnaSynException("Type mismatch. Expected : bool")
    lexical_analyser.acceptKeyword("loop")
    tze1 = tze()
    codeGenerator.addUnite(tze1)
    suiteInstr(lexical_analyser)
    lexical_analyser.acceptKeyword("end")
    tra1 = tra()
    codeGenerator.addUnite(tra1)
    tra1.setAd(ad1)
    tze1.setAd(codeGenerator.getCO())
    logger.debug("end of while loop ")


def altern(lexical_analyser):
    global codeGenerator
    logger.debug("parsing if: ")
    lexical_analyser.acceptKeyword("if")
    
    type = expression(lexical_analyser)
    if(type =='integer'):
        raise AnaSynException("Type mismatch. Expected : bool")
    jump = tze()
    codeGenerator.addUnite(jump)
    lexical_analyser.acceptKeyword("then")
    suiteInstr(lexical_analyser)
    if lexical_analyser.isKeyword("else"):
        lexical_analyser.acceptKeyword("else")
        jump2 = tra()
        codeGenerator.addUnite(jump2)
        jump.setAd(codeGenerator.getCO())
        suiteInstr(lexical_analyser)
        jump=jump2
    jump.setAd(codeGenerator.getCO())
    
    lexical_analyser.acceptKeyword("end")
    logger.debug("end of if")


def retour(lexical_analyser):
    global codeGenerator
    logger.debug("parsing return instruction")
    lexical_analyser.acceptKeyword("return")
    expression(lexical_analyser)


########################################################################
def main():

    parser = argparse.ArgumentParser(
        description='Do the syntactical analysis of a NNP program.')
    parser.add_argument('inputfile', type=str, nargs=1,
                        help='name of the input source file')
    parser.add_argument('-o', '--outputfile', dest='outputfile', action='store',
                        default="", help='name of the output file (default: stdout)')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 1.0')
    parser.add_argument('-d', '--debug', action='store_const', const=logging.DEBUG,
                        default=logging.INFO, help='show debugging info on output')
    parser.add_argument('-p', '--pseudo-code', action='store_const', const=True, default=False,
                        help='enables output of pseudo-code instead of assembly code')
    parser.add_argument('--show-ident-table', action='store_true',
                        help='shows the final identifiers table')
    args = parser.parse_args()

    filename = args.inputfile[0]
    f = None
    try:
        f = open(filename, 'r')
    except:
        print("Error: can\'t open input file!")
        return

    outputFilename = args.outputfile

    # create logger
    LOGGING_LEVEL = args.debug
    logger.setLevel(LOGGING_LEVEL)
    ch = logging.StreamHandler()
    ch.setLevel(LOGGING_LEVEL)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if args.pseudo_code:
        True
    else:
        True

    lexical_analyser = analex.LexicalAnalyser()

    lineIndex = 0
    for line in f:
        line = line.rstrip('\r\n')
        lexical_analyser.analyse_line(lineIndex, line)
        lineIndex = lineIndex + 1
    f.close()

    # launch the analysis of the program
    lexical_analyser.init_analyser()
    program(lexical_analyser)

    if args.show_ident_table:
        print("------ IDENTIFIER TABLE ------")
        print(str(codeGenerator.getSymboleTable()))
        print("------ END OF IDENTIFIER TABLE ------")

    if outputFilename != "":
        try:
            output_file = open(outputFilename, 'w')
        except:
            print("Error: can\'t open output file!")
            return
    else:
        output_file = sys.stdout

    for unite in codeGenerator.compilationUnits:
        print(""+unite.__class__.__name__)
        if unite.__class__.__name__ == 'OperationGenerator':
            for u in unite.compilationUnits:
                print("- "+u.__class__.__name__)

    # Outputs the generated code to a file
    instrIndex = 0
    while instrIndex < len(codeGenerator.compilationUnits):
        output_file.write("%s\n" % str(codeGenerator.get_instruction_at_index(instrIndex)))
        instrIndex += 1

    if outputFilename != "":
        output_file.close()

########################################################################


if __name__ == "__main__":
    main()
