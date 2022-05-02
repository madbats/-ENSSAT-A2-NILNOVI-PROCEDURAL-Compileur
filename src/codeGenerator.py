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
		
class reserver(CompilationUnite):
	params =""
	def constructor(self,n):
		self.params+="#{"+n+"}#"

	def stringify(self,symbols):
		self.params.split("#{"))[1].split("}#")[0]
		
		return 