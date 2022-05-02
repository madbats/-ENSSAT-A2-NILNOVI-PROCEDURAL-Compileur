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