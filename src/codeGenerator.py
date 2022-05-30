#!/usr/bin/python

class Symbole():
	adresse = 0

	bool = False

	def __init__(self,ident,adresse):
		self.ident = ident
		self.adresse = adresse

	def setBool(self,val):
		self.bool = val

	def isBool(self):
		return self.bool
	
	def isInteger(self):
		return not self.bool
	
	def getAdresse(self):
		return self.adresse

	def getIdent(self):
		return self.ident

class CodeGenerator():
	symboleTable = dict()
	compilationUnits=[]
	compteurVariable = 1

	listeIdent = []

	def addUnite(self,unite):
		#print(unite.__class__.__name__)
		self.compilationUnits.append(unite)
	
	def addVariable(self,symbol):
		self.listeIdent.append(Symbole(symbol,self.compteurVariable))
		self.compteurVariable+=1
	
	def setType(self,isBool=False):
		for sym in self.listeIdent:
			sym.setBool(isBool)
			self.symboleTable[sym.getIdent()] = sym

	def addSymbole(self,symbol):
		self.symboleTable[symbol] = len(self.compilationUnits)

	def getSymboleTable(self):
		return self.symboleTable

	def isSymbolTypeBool(self,symbol):
		return self.symboleTable[symbol].isBool()

	def getCO(self):
		return len(self.compilationUnits)

	def get_instruction_at_index(self,index):
		#print(self.compilationUnits[index].__class__.__name__)
		return self.compilationUnits[index].stringify(self.symboleTable)


class CompilationUnite():
	def stringify(self,symbols):
		return False



class debutProg(CompilationUnite):
	params =[]
	def __init__(self):
		return

	def stringify(self,symbols):
		return "debutProg()"

class get(CompilationUnite):

	def stringify(self,symbols):
		return "get()"

class put(CompilationUnite):

	def stringify(self,symbols):
		return "put()"
		

class finProg(CompilationUnite):
	params =[]
	def __init__(self):
		return

	def stringify(self,symbols):
		unite = "finProg()"
		return unite


class reserver(CompilationUnite):
	params =[]
	def __init__(self,n):
		self.params.append(n)

	def stringify(self,symbols):
		unite = "reserver("
		unite +=str(self.params[0])
		unite +=")"
		return unite

class egal(CompilationUnite):

    def stringify(self,symbols):
        return "egal()"

class diff(CompilationUnite):

    def stringify(self,symbols):
        return "diff()"

class inf(CompilationUnite):

    def stringify(self,symbols):
        return "inf()"

class infeg(CompilationUnite):

    def stringify(self,symbols):
        return "infeg()"

class sup(CompilationUnite):

    def stringify(self,symbols):
        return "sup()"

class supeg(CompilationUnite):

    def stringify(self,symbols):
        return "supeg()"



class et(CompilationUnite):

    def stringify(self,symbols):
        return "et()"

class ou(CompilationUnite):

    def stringify(self,symbols):
        return "ou()"

class non(CompilationUnite):

    def stringify(self,symbols):
        return "non()"



class moins(CompilationUnite):

	def stringify(self,symbols):
		return "moins()"

class sous(CompilationUnite):

	def stringify(self,symbols):
		return "sous()"

class add(CompilationUnite):

	def stringify(self,symbols):
		return "add()"

class mult(CompilationUnite):

	def stringify(self,symbols):
		return "mult()"

class div(CompilationUnite):

	def stringify(self,symbols):
		return "div()"

#classes supp pour procédural

class empilerAd(CompilationUnite):
	params =[]
	def constructor(self,n):
		self.params.append(n)
	
	def stringify(self,symbols):
		unite = "empilerAd("
		unite +=str(symbols[self.params[0]].getAdresse().getAdresse())
		unite+=")"
		return unite


class reserverBloc(CompilationUnite):
	params =[]
	
	def stringify(self,symbols):
		unite = "reserverBloc()"
		return unite

class traStat(CompilationUnite):
	params =[]
	def constructor(self,a,nbp):
		self.params.append(a)
		self.params.append(nbp)
	
	def stringify(self,symbols):
		unite = "traStat("
		unite +=str(symbols[self.params[0]].getAdresse())
		unite +=str(symbols[self.params[1]].getAdresse())
		unite+=")"
		return unite

class retourFonct(CompilationUnite):
	params =[]
	
	def stringify(self,symbols):
		unite = "retourFonct()"
		return unite

class retourProc(CompilationUnite):
	params =[]
	
	def stringify(self,symbols):
		unite = "retourProc()"
		return unite

class empilerParam(CompilationUnite):
	params =[]
	def constructor(self,ad):
		self.params.append(ad)
	
	def stringify(self,symbols):
		unite = "empilerParam("
		unite +=str(symbols[self.params[0]].getAdresse())
		unite+=")"
		return unite


class empiler(CompilationUnite):
	def __init__(self,val,hasSymbol=True):
		self.params = [val]
		self.hasSymbol = hasSymbol

	def stringify(self,symbols):
		unite = "empiler("
		if(self.hasSymbol):
			#print("has: "+str(self.params[0])+"->"+str(symbols[self.params[0]].getAdresse()))
			unite += str(symbols[self.params[0]].getAdresse())
		else:
			#print("no: "+str(self.params[0]))
			#print("->"+str(symbols[self.params[0]].getAdresse()))
			unite += str(self.params[0])
		unite+=")"
		return unite


class affectation(CompilationUnite):
	params =[]

	def stringify(self,symbols):
		unite = "affectation()"
		return unite

class valeurPile(CompilationUnite):
	params =[]
	
	def stringify(self,symbols):
		unite = "valeurPile("
		# unite +=str(symbols[self.params[0]].getAdresse())
		unite+=")"
		return unite


class tra(CompilationUnite):
	params =[]
	
	# init pour un saut vers un symbol
	def __init__(self,ad):
		self.hasSymbol = True
		self.params.append(ad)
	
	# init pour un saut vers un point plus loin dans le code
	def __init__(self,ad):
		self.hasSymbol = True
		self.params=[ad]
	
	def __init__(self):
		self.hasSymbol = False

	def setAd(self,ad):
		self.params = [ad]

	def stringify(self,symbols):
		unite = "tra("
		unite += str(symbols[self.params[0]].getAdresse()) if (self.hasSymbol) else str(self.params[0])
		unite += ")"
		
		return unite

class tze(CompilationUnite):
	params =[]

	def __init__(self,ad):
		self.hasSymbol = True
		self.params=[ad]
	
	def __init__(self):
		self.hasSymbol = False

	def setAd(self,ad):
		self.params = [ad]

	def stringify(self,symbols):
		unite = "tze("
		unite += str(symbols[self.params[0]].getAdresse()) if (self.hasSymbol) else str(self.params[0])
		unite += ")"
		return unite

		
class erreur(CompilationUnite):
	params =[]
	def __init__(self,n):
		self.params.append(n)

	def stringify(self,symbols):
		unite = "erreur("
		unite += str(symbols[self.params[0]].getAdresse())
		unite += ")"
		
		return unite