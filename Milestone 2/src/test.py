import os,sys
import time
import clex
import ply.yacc as yacc
from SymbolTable import *
from decode import *


global currentSymbolTable
currentSymbolTable = SymbolTable(-1)
global FUNCTION_PROTOTYPE_DECLARATION
FUNCTION_PROTOTYPE_DECLARATION = [{'NAME':' ','INPUT':'',"OUTPUT":''}]
global functions
functions = []
global parametersymboltable
parametersymboltable = SymbolTable(-1)
tableNumber = 1;

if __name__ == "__main__":
	t2 = ['a','b','c']
	t = {'NODE_TYPE':'var_declaration','VAR_TYPE':'INT', 'VAR_LIST': t2}
	for x in t2:
		if (currentSymbolTable.insert(x['ID'],{'TYPE':'INT','STATIC':0,'ARRAY': x['ARRAY'],'INDEX1':0,'INDEX2':0,'SCOPETYPE':'GLOBAL'}) == False):
			print x['ID'],': Variable already declared '
			sys.exit()
		else:
			x['SCOPETYPE'] = 'GLOBAL'
			check = currentSymbolTable.lookupCurrentTable(x['ID'])
			#print check
			x['TYPE'] = t[1]['TYPE']
			x['offset'] = check['offset']
			x['STATIC'] = 0