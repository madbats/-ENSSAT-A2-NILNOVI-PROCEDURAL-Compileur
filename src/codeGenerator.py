#!/usr/bin/python

from copyreg import constructor
import sys
import argparse
import re
import logging

class CodeGenerator(Object):
	symboleTable = []
	compilationUnits=[]

	def addUnite(self,unite):
		self.compilationUnits.append(unite)
	

class CompilationUnite(Object):
	def stringify(symbols):
		return False



class debutProg(CompilationUnite):

	def stringify(symbols):
		return "debutProg()"

class get(CompilationUnite):

	def stringify(symbols):
		return "get()"

class put(CompilationUnite):

	def stringify(symbols):
		return "put()"
		
class reserver(CompilationUnite):
    params =[]
    def __init__(self,n):
        self.params.append(n)

    def stringify(self,symbols):
        unite = "reserver("
        for param in self.params:
            unite+=str(symbols[param])+","
        if unite[-1]==",":
            unite[-1]=")"
        else:
            unite+=")"
        return unite



class egal(CompilationUnite):

    def stringify(symbols):
        return "egal()"

class diff(CompilationUnite):

    def stringify(symbols):
        return "diff()"

class inf(CompilationUnite):

    def stringify(symbols):
        return "inf()"

class infeg(CompilationUnite):

    def stringify(symbols):
        return "infeg()"

class sup(CompilationUnite):

    def stringify(symbols):
        return "sup()"

class supeg(CompilationUnite):

    def stringify(symbols):
        return "supeg()"



class et(CompilationUnite):

    def stringify(symbols):
        return "et()"

class ou(CompilationUnite):

    def stringify(symbols):
        return "ou()"

class non(CompilationUnite):

    def stringify(symbols):
        return "non()"



class moins(CompilationUnite):

	def stringify(symbols):
		return "moins()"

class sous(CompilationUnite):

	def stringify(symbols):
		return "sous()"

class add(CompilationUnite):

	def stringify(symbols):
		return "add()"

class mult(CompilationUnite):

	def stringify(symbols):
		return "mult()"

class div(CompilationUnite):

	def stringify(symbols):
		return "div()"

#classes supp pour procédural

class empilerAdd(CompilationUnite):
	params =[]
	def constructor(self,n):
		self.params.append(n)
	
	def stringify(self,symbols):
		unite = "empilerAdd("
		for param in self.params:
			unite+=str(symbols[param])+","
		if unite[-1]==",":
			unite[-1]=")"
		else:
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
		unite = "empilerAdd("
		for param in self.params:
			unite+=str(symbols[param])+","
		if unite[-1]==",":
			unite[-1]=")"
		else:
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
		for param in self.params:
			unite+=str(symbols[param])+","
		if unite[-1]==",":
			unite[-1]=")"
		else:
			unite+=")"
		return unite
        

class tra(CompilationUnite):
	params =[]
	def __init__(self,ad):
		self.params.append(ad)

   	def stringify(self,symbols):
		unite = "tra("
		unite += str(symbols[self.params[0]])
		unite += ")"
		
		return unite

class tze(CompilationUnite):
	params =[]
	def __init__(self,ad):
		self.params.append(ad)

	def stringify(self,symbols):
		unite = "tze("
		unite += str(symbols[self.params[0]])
		unite += ")"
		
		return unite

		
class erreur(CompilationUnite):
	params =[]
	def __init__(self,n):
		self.params.append(n)

	def stringify(self,symbols):
		unite = "erreur("
		unite += str(symbols[self.params[0]])
		unite += ")"
		
		return unite
		
		unite = "tra("