import sys
import os
import lexer
import ply.yacc as yacc
import createParseTree
import SymbolTable

from createParseTree import create_tree
from createParseTree import calc_tree
from createParseTree import tokenVal
from SymbolTable import *


global declarationType
declarationType = 0		#0 default 1 for var declaraion -1 for func declaration
global functionDefinition
functionDefinition = 0  #0 default 1 if it is a function defintion

global returnSpecifier
returnSpecifier = 'void'

global currentSymbolTable
currentSymbolTable = SymbolTable(-1)
global FUNCTION_PROTOTYPE_DECLARATION
FUNCTION_PROTOTYPE_DECLARATION = [{'NAME':' ','INPUT':'',"OUTPUT":''}]
global FUNCTION_PROTOTYPE_DEFINITION
FUNCTION_PROTOTYPE_DEFINITION = [{'NAME':' ','INPUT':'',"OUTPUT":''}]
global functions
functions = []
global parametersymboltable
parametersymboltable = SymbolTable(-1)
tableNumber = 1;
type = ''

tokens = lexer.tokens
flag_for_error = 0

def p_translation_unit(p):
	'''translation_unit : external_declaration
						| translation_unit external_declaration '''
	#print "translational_unit"
	#p[0]=("translational_unit",)+tuple(p[-len(p)+1:])

def p_primary_expression(p):
	'''primary_expression : constant
							| string '''
	#print "primary_expression"
	#p[0]=("primary_expression",)+tuple(p[-len(p)+1:])
	p[0] = p[1]

def p_primary_expression2(p):
	'''primary_expression : LPAREN expression RPAREN
							| generic_selection '''
	#print "primary_expression"
	#p[0]=("primary_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 4):
		p[0] = p[2]
	else:
		print "Rule not added"

def p_primary_expression3(p):
	'''primary_expression : IDENTIFIER  '''
	flag = 0
	check = currentSymbolTable.lookup(p[1])
	if(check == False):
		check = parametersymboltable.lookup(p[1])
		if(check == False):
			for func in FUNCTION_PROTOTYPE_DEFINITION :
				if(p[1] in func['NAME']):
					flag = 1
					break
			if(flag == 0):
				print "ERROR at line number ", p.lineno(1) ,": parameter Variable not declared: ", p[1]
				sys.exit()
	if(flag == 0):
		p[0] = check['attributes']
	else:
		p[0] = func
	#print "primary_expression"
	#p[0]=("primary_expression",)+tuple(p[-len(p)+1:])

def p_constant(p):
	'''constant : I_CONSTANT '''
	#print "constant"
	#p[0]=("primary_expression",)+tuple(p[-len(p)+1:])
	p[0] = {'INDEX2': '', 'INDEX1': '', 'ARRAY': 0, 'TYPE':'int'}

def p_constant2(p):
	'''constant : F_CONSTANT '''
	#print "constant"
	#p[0]=("primary_expression",)+tuple(p[-len(p)+1:])
	p[0] = {'INDEX2': '', 'INDEX1': '', 'ARRAY': 0, 'TYPE':'float'}

def p_constant3(p):
	'''constant : CCONST '''
	#print "constant"
	#p[0]=("primary_expression",)+tuple(p[-len(p)+1:])
	p[0] = {'INDEX2': '', 'INDEX1': '', 'ARRAY': 0, 'TYPE':'char'}

def p_enumeration_constant(p):
	'''enumeration_constant : IDENTIFIER'''
	#print "enumeration_constant"
	#p[0]=("enumeration_constant",)+tuple(p[-len(p)+1:])

def p_string(p):
	'''string : STRINGLITERAL
				| FUNC_NAME '''
	print "doubt"
	#p[0]=("string",)+tuple(p[-len(p)+1:])
	p[0] = {'INDEX2': '', 'INDEX1': '', 'ARRAY': 1, 'TYPE':'char'}

def p_generic_selection(p):
	'''generic_selection : GENERIC LPAREN assignment_expression COMMA generic_assoc_list RPAREN '''
	#print "generic_selection"
	#p[0]=("generic_selection",)+tuple(p[-len(p)+1:])
	
def p_generic_assoc_list(p):
	'''generic_assoc_list : generic_association
							| generic_assoc_list COMMA generic_association '''
	#print "generic_assoc_list"
	#p[0]=("generic_assoc_list",)+tuple(p[-len(p)+1:])
	
def p_generic_association(p):
	'''generic_association : type_name COLON assignment_expression
							| DEFAULT COLON assignment_expression '''
	#print "generic_association"
	#p[0]=("generic_association",)+tuple(p[-len(p)+1:])
		
def p_postfix_expression(p):
	'''postfix_expression : primary_expression
							| postfix_expression LBRACKET expression RBRACKET'''
	#print "postfix_expresssion"
	#p[0]=("postfix_expresssion",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	else:
		print "rule not added"


def p_postfix_expression2(p):
	'''postfix_expression : postfix_expression LPAREN RPAREN
							| postfix_expression LPAREN argument_expression_list RPAREN'''
	#print "postfix_expresssion"
	#p[0]=("postfix_expresssion",)+tuple(p[-len(p)+1:])
	if(len(p) == 4):
		p[0] = p[1]
		if(str(p[1]['INPUT'][0]) != "void"):
			print "Error at line number", p.lineno(1) ,": insufficient function arguments for function ",p[1]['NAME']
			sys.exit()
	else:
		if(str(p[1]['INPUT']) == str(p[3])):
			p[0] = p[1]
		else:
			print "Error at line number", p.lineno(1) ,": invalid function arguments for function ",p[1]['NAME']
			sys.exit()


def p_postfix_expression3(p):
	'''postfix_expression : postfix_expression PERIOD IDENTIFIER
							| postfix_expression PTR_OP IDENTIFIER
							| postfix_expression INC_OP
							| postfix_expression DEC_OP
							| LPAREN type_name RPAREN left_brace initializer_list right_brace
							| LPAREN type_name RPAREN left_brace initializer_list COMMA right_brace '''
	#print "postfix_expresssion"
	#p[0]=("postfix_expresssion",)+tuple(p[-len(p)+1:])
	

def p_argument_expression_list(p):
	'''argument_expression_list : assignment_expression
								| argument_expression_list COMMA assignment_expression '''
	#print "argument_expression_list"
	#p[0]=("argument_expression_list",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		if(p[1].has_key('TYPE')):
			p[0] = [p[1]['TYPE']]
		else:
			p[0] = [p[1]['OUTPUT']]
	else:
		if(p[3].has_key('TYPE')):
			p[0] = p[1] + [p[3]['TYPE']]
		else:
			p[0] = p[1] + [p[3]['OUTPUT']]

def p_unary_expression(p):
	'''unary_expression : postfix_expression
						| INC_OP unary_expression
						| DEC_OP unary_expression
						| unary_operator cast_expression
						| SIZEOF unary_expression
						| SIZEOF LPAREN type_name RPAREN
						| ALIGNOF LPAREN type_name RPAREN '''
	#print "unary_expression"
	#p[0]=("unary_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]

def p_unary_operator(p):
	'''unary_operator : AND_OP
						| TIMES
						| PLUS
						| MINUS
						| NOT_OP
						| LNOT '''     #changetoken
	#print "unary_operator"
	#p[0]=("unary_operator",)+tuple(p[-len(p)+1:])
		
def p_cast_expression(p):
	'''cast_expression : unary_expression
						| LPAREN type_name RPAREN cast_expression '''
	#print "cast_expression"
	#p[0]=("cast_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	else:
		p[0] = {'TYPE':p[2]['TYPE']}


def p_multiplicative_expression(p):
	'''multiplicative_expression : cast_expression
								 | multiplicative_expression TIMES cast_expression
								 | multiplicative_expression DIVIDE cast_expression 
								 | multiplicative_expression MOD cast_expression '''
	#print "multiplicative_expression"
	#p[0]=("multiplicative_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	else:
		if(p[1]['TYPE'] == p[3]['TYPE']):
			p[0] = {'TYPE':p[1]['TYPE']}
		else:
			print "Error at line number", p.lineno(1) ,": mismatched type"
			sys.exit()

def p_additive_expression(p):
	'''additive_expression : multiplicative_expression
							| additive_expression PLUS multiplicative_expression
							| additive_expression MINUS multiplicative_expression '''
	#print "additive_expression"
	#p[0]=("additive_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	else:
		if(p[1]['TYPE'] == p[3]['TYPE']):
			p[0] = {'TYPE':p[1]['TYPE']}
		else:
			print "Error at line number", p.lineno(1) ,": mismatched type"
			sys.exit()

def p_shift_expression(p):
	'''shift_expression : additive_expression
						| shift_expression LEFT_OP additive_expression
						| shift_expression RIGHT_OP additive_expression '''
	#print "shift_expression"
	#p[0]=("shift_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]

def p_relational_expression(p):
	'''relational_expression : shift_expression
								| relational_expression LT_OP shift_expression
								| relational_expression GT_OP shift_expression
								| relational_expression LE_OP shift_expression
								| relational_expression GE_OP shift_expression '''
	#print "relational_expression"
	#p[0]=("relational_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]

def p_equality_expression(p):
	'''equality_expression : relational_expression
							| equality_expression EQ_OP relational_expression
							| equality_expression NE_OP relational_expression '''
	#print "equality_expression"
	#p[0]=("equality_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]

def p_and_expression(p):
	'''and_expression : equality_expression
						| and_expression AND_OP equality_expression '''
	#print "and_expression"
	#p[0]=("and_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	
def p_exclusive_or_expression(p):
	'''exclusive_or_expression : and_expression
								| exclusive_or_expression XOR and_expression '''
	#print "exclusive_or_expression"
	#p[0]=("exclusive_or_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	
def p_inclusive_or_expression(p):
	'''inclusive_or_expression : exclusive_or_expression
								| inclusive_or_expression OR_OP exclusive_or_expression '''
	#print "inclusive_or_expression"
	#p[0]=("inclusive_or_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]

def p_logical_and_expression(p):
	'''logical_and_expression : inclusive_or_expression
								| logical_and_expression LAND inclusive_or_expression '''
	#print "logical_and_expression"
	#p[0]=("logical_and_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]

def p_logical_or_expression(p):
	'''logical_or_expression : logical_and_expression
								| logical_or_expression LOR logical_and_expression '''
	#print "logical_or_expression"
	#p[0]=("logical_or_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	else:
		print "Rule not added logical_or_expression"
	
def p_conditional_expression(p):
	'''conditional_expression : logical_or_expression
								| logical_or_expression CONDOP expression COLON conditional_expression '''
	#print "conditional_expression"
	#p[0]=("conditional_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	else:
		print "Rule not added conditional_expression"

def p_assignment_expression(p):
	'''assignment_expression : conditional_expression
								| unary_expression assignment_operator assignment_expression '''
	#print "assignment_expression"
	#p[0]=("assignment_expression",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	else:
		if(str(p[1]['TYPE']) == str(p[3]['TYPE'])):
			p[0] = {'TYPE': p[1]['TYPE']}
		else:
			print "Error at line number", p.lineno(2) ,": type mismatch in assignment"
			sys.exit()

def p_assignment_operator(p):
	'''assignment_operator : EQUALS 
							| MUL_ASSIGN
							| DIV_ASSIGN
							| MOD_ASSIGN
							| ADD_ASSIGN
							| SUB_ASSIGN
							| LEFT_ASSIGN
							| RIGHT_ASSIGN
							| AND_ASSIGN
							| XOR_ASSIGN
							| OR_ASSIGN
							 '''                         #changetoken
	#print "assignment_operator"
	#p[0]=("assignment_operator",)+tuple(p[-len(p)+1:])
	p[0] = p[1]

def p_expression(p):
	'''expression : assignment_expression
					| expression COMMA assignment_expression '''
	#print "expression"
	#p[0]=("expression",)+tuple(p[-len(p)+1:])
	p[0] = p[1]

def p_constant_expression(p):
	'''constant_expression : conditional_expression'''
	#print "constant_expression"
	#p[0]=("constant_expression",)+tuple(p[-len(p)+1:])
	
def p_declaration(p):
	'''declaration : declaration_specifiers SEMI
					| declaration_specifiers init_declarator_list SEMI
					| static_assert_declaration '''
	#print "declaration"
	#print dict
	global declarationType
	global FUNCTION_PROTOTYPE_DECLARATION
	global FUNCTION_PROTOTYPE_DEFINITION
	if(declarationType == 1) :
		for x in p[2]:
			if(x.has_key('TYPE')):
				if(x['TYPE'] != p[1]['TYPE']):
					print "Error at line number", p.lineno(2) ,": invalid assignment"


		for x in p[2]:
			if (currentSymbolTable.insert(x['ID'],{'TYPE':p[1]['TYPE'],'STATIC':0,'ARRAY': x['ARRAY'],'INDEX1':x['INDEX1'],'INDEX2':x['INDEX2'],'SCOPETYPE':'GLOBAL'}) == False):
				print x['ID'],': Variable already declared '
				sys.exit()
			else:
				x['SCOPETYPE'] = 'GLOBAL'
				check = currentSymbolTable.lookupCurrentTable(x['ID'])
				#print check
				x['TYPE'] = p[1]['TYPE']
				x['offset'] = check['offset']
				x['STATIC'] = 0
				#print "current"
				#print currentSymbolTable.symbols
	else:
		inp=[]
		if(len(p[2][0]) == 1):
			inp = ['void']
		else:
			for i in p[2][0][1]:
				inp=inp+[i[0]['TYPE']]
		p[0] = {'NODE_TYPE':'function_definition', 'OUTPUT':p[1]['TYPE'], 'INPUT': inp, 'IDENTIFIER': p[2][0][0],'partProgram':''}
		#print p[2][1][0]
		flag = 0
		for func in FUNCTION_PROTOTYPE_DECLARATION :
				if(p[2][0][0] in func['NAME'] or p[2][0][0] == 'main'):
					print "Error at line number", p.lineno(1) ,":function already declared"
					flag = 1
					break
		for func in FUNCTION_PROTOTYPE_DEFINITION :
				if(p[2][0][0] in func['NAME'] or p[2][0][0] == 'main'):
					print "Error at line number", p.lineno(1) ,":function already declared"
					flag = 1
					break
		#print p[2][1][0]
		if(flag != 1):
			CURRENT_DECLARATION = [{"NAME":p[2][0][0],"INPUT":inp,"OUTPUT":p[1]['TYPE']}]
			FUNCTION_PROTOTYPE_DECLARATION = FUNCTION_PROTOTYPE_DECLARATION + CURRENT_DECLARATION
			parametersymboltable = SymbolTable(-1)	
	declarationType = 0

	#p[0]=("declaration",)+tuple(p[-len(p)+1:])
		
def p_declaration_specifiers(p):
	'''declaration_specifiers : storage_class_specifier declaration_specifiers
								| storage_class_specifier
								| type_specifier declaration_specifiers
								| type_specifier
								| type_qualifier declaration_specifiers
								| type_qualifier
								| function_specifier declaration_specifiers
								| function_specifier
								| alignment_specifier declaration_specifiers
								| alignment_specifier '''
	#print "declaration_specifiers"
	#p[0]=("declaration_specifiers",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	
def p_init_declarator_list(p):
	'''init_declarator_list : init_declarator
							| init_declarator_list COMMA init_declarator '''
	#print "init_declarator_list"
	#p[0]=("init_declarator_list",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[3]];

def p_init_declarator(p):
	'''init_declarator : declarator EQUALS initializer
						| declarator '''
	#print "init_declarator"
	#p[0]=("init_declarator",)+tuple(p[-len(p)+1:])
	if(len(p) == 4):
		if(p[3].has_key('TYPE')):
			p[0] = {'INDEX2': p[1]['INDEX2'], 'NODE_TYPE': 'var_decl_id', 'INDEX1': p[1]['INDEX1'], 'ARRAY': p[1]['ARRAY'], 'ID': p[1]['ID'], 'TYPE':p[3]['TYPE']}
		else:
			p[0] = {'INDEX2': p[1]['INDEX2'], 'NODE_TYPE': 'var_decl_id', 'INDEX1': p[1]['INDEX1'], 'ARRAY': p[1]['ARRAY'], 'ID': p[1]['ID'], 'TYPE':p[3]['OUTPUT']}
	else:
		p[0] = p[1]
		
def p_storage_class_specifier(p):
	'''storage_class_specifier : TYPEDEF
								| EXTERN
								| STATIC
								| THREAD_LOCAL
								| AUTO
								| REGISTER '''
	#print "storage_class_specifier"
	#p[0]=("storage_class_specifier",)+tuple(p[-len(p)+1:])
	
def p_type_specifier(p):
	'''type_specifier : VOID
						| CHAR 
						| SHORT
						| INT 
						| LONG
						| FLOAT
						| DOUBLE
						| SIGNED
						| UNSIGNED
						| BOOL
						| COMPLEX
						| IMAGINARY
						| TYPEID '''
	#print "type_specifier"
	p[0] = {'NODE_TYPE': 'type_specifier', 'TYPE': p[1]}
	#p[0]=("type_specifier",)+tuple(p[-len(p)+1:])

def p_type_specifier2(p):
	'''type_specifier : struct_or_union_specifier
						| enum_specifier '''
	#print "type_specifier"
	#p[0]=("type_specifier",)+tuple(p[-len(p)+1:])
	print "struct rules"

def p_struct_or_union_specifier(p):
	'''struct_or_union_specifier : struct_or_union left_brace struct_declaration_list right_brace
								| struct_or_union IDENTIFIER left_brace struct_declaration_list right_brace
								| struct_or_union IDENTIFIER '''
	#print "struct_or_union_specifier"
	#p[0]=("struct_or_union_specifier",)+tuple(p[-len(p)+1:])
	
def p_struct_or_union(p):
	'''struct_or_union : STRUCT
						| UNION '''
	#print "struct_or_union"
	#p[0]=("struct_or_union",)+tuple(p[-len(p)+1:])
	
def p_struct_declaration_list(p):
	'''struct_declaration_list : struct_declaration
								| struct_declaration_list struct_declaration '''
	#print "struct_declaration_list"
	#p[0]=("struct_declaration_list",)+tuple(p[-len(p)+1:])
	
def p_struct_declaration(p):
	'''struct_declaration : specifier_qualifier_list SEMI 
							| specifier_qualifier_list struct_declarator_list SEMI
							| static_assert_declaration '''
	#print "struct_declaration"
	#p[0]=("struct_declaration",)+tuple(p[-len(p)+1:])

def p_specifier_qualifier_list(p):
	'''specifier_qualifier_list : type_specifier specifier_qualifier_list
								| type_specifier
								| type_qualifier specifier_qualifier_list
								| type_qualifier '''
	#print "specifier_qualifier_list"
	#p[0]=("specifier_qualifier_list",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	
def p_struct_declarator_list(p):
	'''struct_declarator_list : struct_declarator
								| struct_declarator_list COMMA struct_declarator '''
	#print "struct_declarator_list"
	#p[0]=("struct_declarator_list",)+tuple(p[-len(p)+1:])                       #changetoken
	
def p_struct_declarator(p):
	'''struct_declarator : COLON constant_expression
							| declarator COLON constant_expression
							| declarator '''
	#print "struct_declarator"
	#p[0]=("struct_declarator",)+tuple(p[-len(p)+1:])                        #changetoken
	
def p_enum_specifier(p):
	'''enum_specifier : ENUM left_brace enumerator_list right_brace
						| ENUM left_brace enumerator_list COMMA right_brace
						| ENUM IDENTIFIER left_brace enumerator_list right_brace
						| ENUM IDENTIFIER left_brace enumerator_list COMMA right_brace
						| ENUM IDENTIFIER '''
	#print "enum_specifier"
	#p[0]=("enum_specifier",)+tuple(p[-len(p)+1:])                        #changetoken
	
def p_enumerator_list(p):
	'''enumerator_list : enumerator
						| enumerator_list COMMA enumerator '''
	#print "enumerator_list"
	#p[0]=("enumerator_list",)+tuple(p[-len(p)+1:])                        #changetoken
	
def p_enumerator(p):
	'''enumerator : enumeration_constant EQUALS constant_expression
					| enumeration_constant '''
	#print "enumerator"
	#p[0]=("enumerator",)+tuple(p[-len(p)+1:])                      
	
def p_type_qualifier(p):
	'''type_qualifier : CONST
						| RESTRICT
						| VOLATILE
						'''
	#print "type_qualifier"
	#p[0]=("type_qualifier",)+tuple(p[-len(p)+1:])
	
def p_function_specifier(p):
	'''function_specifier : INLINE
							| NORETURN '''
	#print "function_specifier"
	#p[0]=("function_specifier",)+tuple(p[-len(p)+1:])
	
def p_alignment_specifier(p):
	'''alignment_specifier : ALIGNAS LPAREN type_name RPAREN 
							| ALIGNAS LPAREN constant_expression RPAREN '''
	#print "alignment_specifier"
	#p[0]=("alignment_specifier",)+tuple(p[-len(p)+1:])
	
def p_declarator(p):
	'''declarator : pointer direct_declarator
					| direct_declarator '''
	#print "declarator"
	#p[0]=("declarator",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]

def p_direct_declarator(p):
	'''direct_declarator : IDENTIFIER
							| IDENTIFIER LBRACKET arrayindex RBRACKET
							| IDENTIFIER LBRACKET arrayindex RBRACKET LBRACKET arrayindex RBRACKET '''
	#print "direct_declarator"
	global declarationType
	declarationType = 1
	if(len(p) == 2 ):
		p[0] = {'NODE_TYPE' : 'var_decl_id', 'ARRAY':0, 'ID' : p[1], 'INDEX1': '','INDEX2':''}
	elif(len(p) == 5):
		p[0] = {'NODE_TYPE': 'var_decl_id','ARRAY':1, 'ID' : p[1], 'INDEX1': p[3],'INDEX2':''}
	else:
		p[0] = {'NODE_TYPE': 'var_decl_id','ARRAY':2, 'ID' : p[1], 'INDEX1': p[3],'INDEX2':p[6]}
		#print t[1]
	#p[0]=("direct_declarator",)+tuple(p[-len(p)+1:])

def p_arrayindex(p):
	'''arrayindex : IDENTIFIER
				| I_CONSTANT '''
	p[0] = p[1]

def p_direct_declarator2(p):
	'''direct_declarator : IDENTIFIER LBRACKET RBRACKET
							| IDENTIFIER LBRACKET RBRACKET LBRACKET RBRACKET
							| IDENTIFIER LBRACKET RBRACKET LBRACKET arrayindex RBRACKET '''
	#print "direct_declarator"
	global declarationType
	declarationType = 1
	if(len(p) == 4 ):
		p[0] = {'NODE_TYPE' : 'var_decl_id', 'ARRAY':1, 'ID' : p[1], 'INDEX1': '0','INDEX2':''}
	elif(len(p) == 6):
		p[0] = {'NODE_TYPE': 'var_decl_id','ARRAY':2, 'ID' : p[1], 'INDEX1': '0','INDEX2':'0'}
	else:
		p[0] = {'NODE_TYPE': 'var_decl_id','ARRAY':2, 'ID' : p[1], 'INDEX1': '0','INDEX2':p[5]}


def p_direct_declarator3(p):
	'''direct_declarator : IDENTIFIER LPAREN parameter_type_list RPAREN
							| IDENTIFIER LPAREN RPAREN '''
	#print "direct_declarator"
		#print t[1]
	#p[0]=("direct_declarator",)+tuple(p[-len(p)+1:])
	global declarationType
	declarationType = -1

	if(len(p)==5):
		p[0] = [p[1]]+[p[3]]
	
	if(len(p)==4):
		p[0] = [p[1]]



def p_pointer(p):
	'''pointer : TIMES type_qualifier_list pointer
				| TIMES type_qualifier_list 
				| TIMES pointer
				| TIMES '''
	#print "pointer"
	#p[0]=("pointer",)+tuple(p[-len(p)+1:])
	
def p_type_qualifier_list(p):
	'''type_qualifier_list : type_qualifier
							| type_qualifier_list type_qualifier '''
	#print "type_qualifier_list"
	#p[0]=("type_qualifier_list",)+tuple(p[-len(p)+1:])
	
def p_parameter_type_list(p):
	'''parameter_type_list : parameter_list '''
	#print "parameter_type_list"
	#p[0]=("parameter_type_list",)+tuple(p[-len(p)+1:])
	p[0]=p[1]

def p_parameter_list(p):
	'''parameter_list : parameter_declaration
						| parameter_list COMMA parameter_declaration '''
	#print "parameter_list"
	#p[0]=("parameter_list",)+tuple(p[-len(p)+1:])
	#print p[1]
	if(len(p)==2):
		p[0]=[p[1]]
		if(len(p[1]) > 1):
			parametersymboltable.insert(p[1][1]['ID'],{'TYPE':p[1][0]['TYPE'],'ARRAY':p[1][1]['ARRAY'],'SCOPETYPE':'PARAMETER','INDEX1':0,'STATIC':0})

	if(len(p)==4):
		p[0]=p[1]+[p[3]]
		if(len(p[3]) > 1):
			parametersymboltable.insert(p[3][1]['ID'],{'TYPE':p[3][0]['TYPE'],'ARRAY':p[3][1]['ARRAY'],'SCOPETYPE':'PARAMETER','INDEX1':0,'STATIC':0})
	#print "para---"
	#print parametersymboltable.symbols


def p_parameter_declaration(p):
	'''parameter_declaration : declaration_specifiers declarator
								| declaration_specifiers abstract_declarator
								| declaration_specifiers '''
	#print "parameter_declaration"
	#p[0]=("parameter_declaration",)+tuple(p[-len(p)+1:])
	if(len(p)==3):
		p[0]=[p[1]]+[p[2]]
	
	if(len(p)==2):
		p[0]=[p[1]]	

def p_identifier_list(p):
	'''identifier_list : IDENTIFIER
						| identifier_list COMMA IDENTIFIER '''
	#print "identifier_list"
	#p[0]=("identifier_list",)+tuple(p[-len(p)+1:])
	
def p_type_name(p):
	'''type_name : specifier_qualifier_list abstract_declarator
					| specifier_qualifier_list '''
	#print "type_name"
	#p[0]=("type_name",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]
	
def p_abstract_declarator(p):
	'''abstract_declarator : pointer direct_abstract_declarator
							| pointer
							| direct_abstract_declarator '''
	#print "abstarct_declarator"
	#p[0]=("abstarct_declarator",)+tuple(p[-len(p)+1:])
	
def p_direct_abstract_declarator(p):
	'''direct_abstract_declarator : LPAREN abstract_declarator RPAREN 
									| LBRACKET RBRACKET
									| LBRACKET TIMES RBRACKET 
									| LBRACKET STATIC type_qualifier_list assignment_expression RBRACKET 
									| LBRACKET STATIC assignment_expression RBRACKET 
									| LBRACKET type_qualifier_list STATIC assignment_expression RBRACKET 
									| LBRACKET type_qualifier_list assignment_expression RBRACKET 
									| LBRACKET type_qualifier_list RBRACKET 
									| LBRACKET assignment_expression RBRACKET 
									| direct_abstract_declarator LBRACKET RBRACKET
									| direct_abstract_declarator LBRACKET TIMES RBRACKET
									| direct_abstract_declarator LBRACKET STATIC type_qualifier_list assignment_expression RBRACKET
									| direct_abstract_declarator LBRACKET STATIC assignment_expression RBRACKET
									| direct_abstract_declarator LBRACKET type_qualifier_list assignment_expression RBRACKET
									| direct_abstract_declarator LBRACKET type_qualifier_list STATIC assignment_expression RBRACKET 
									| direct_abstract_declarator LBRACKET type_qualifier_list RBRACKET
									| direct_abstract_declarator LBRACKET assignment_expression RBRACKET
									| LPAREN RPAREN 
									| LPAREN parameter_type_list RPAREN 
									| direct_abstract_declarator LPAREN RPAREN
									| direct_abstract_declarator LPAREN parameter_type_list RPAREN
									 '''
	#print "direct_abstract_declarator"
	#p[0]=("direct_abstract_declarator",)+tuple(p[-len(p)+1:])
	
def p_initializer(p):
	'''initializer : left_brace initializer_list right_brace
					| left_brace initializer_list COMMA right_brace 
					| assignment_expression '''
	#print "initializer"
	#p[0]=("initializer",)+tuple(p[-len(p)+1:])
	if(len(p) == 2):
		p[0] = p[1]

def p_initializer_list(p):
	'''initializer_list : designation initializer
						| initializer
						| initializer_list COMMA designation initializer
						| initializer_list COMMA initializer
						'''
	#print "initializer_list"
	#p[0]=("initializer_list",)+tuple(p[-len(p)+1:])
	
def p_designation(p):
	'''designation : designator_list EQUALS '''
	#print "designation"
	#p[0]=("designation",)+tuple(p[-len(p)+1:])
	
def p_designator_list(p):
	'''designator_list : designator
						| designator_list designator '''
	#print "designator_list"
	#p[0]=("designator_list",)+tuple(p[-len(p)+1:])
	
def p_designator(p):
	'''designator : LBRACKET constant_expression RBRACKET 
					| PERIOD IDENTIFIER '''
	#print "designator"
	#p[0]=("designator",)+tuple(p[-len(p)+1:])
	
def p_static_assert_declaration(p):
	'''static_assert_declaration : STATIC_ASSERT LPAREN constant_expression COMMA STRINGLITERAL RPAREN SEMI '''
	#print "static_assert_declaration"
	#p[0]=("static_assert_declaration",)+tuple(p[-len(p)+1:])
	
def p_statement(p):
	'''statement : labeled_statement
					| compound_statement
					| expression_statement
					| selection_statement
					| iteration_statement
					| jump_statement '''
	#print "statement"
	#p[0]=("statement",)+tuple(p[-len(p)+1:])
	
def p_labeled_statement(p):
	'''labeled_statement : IDENTIFIER COLON statement
						| CASE constant_expression COLON statement
						| DEFAULT COLON statement
						 '''
	#print "labeled_statement"
	#p[0]=("labeled_statement",)+tuple(p[-len(p)+1:])
	
def p_compound_statement(p):
	'''compound_statement : left_brace right_brace 
							| left_brace block_item_list right_brace '''
	#print "compound_statement"
	#p[0]=("compound_statement",)+tuple(p[-len(p)+1:])
	
def p_block_item_list(p):
	'''block_item_list : block_item
						| block_item_list block_item '''
	#print "block_item_list"
	#p[0]=("block_item_list",)+tuple(p[-len(p)+1:])
	
def p_block_item(p):
	'''block_item : declaration
					| statement '''
	#print "block_item"
	#p[0]=("block_item",)+tuple(p[-len(p)+1:])
	
def p_expression_statement(p):
	'''expression_statement : SEMI 
							| expression SEMI  '''
	#print "expression_statement"
	#p[0]=("expression_statement",)+tuple(p[-len(p)+1:])

def p_selection_statement(p):
	'''selection_statement : IF LPAREN expression RPAREN statement ELSE statement
							| IF LPAREN expression RPAREN statement  
							| SWITCH LPAREN expression RPAREN statement '''
	#print "selection_statement"
	#p[0]=("selection_statement",)+tuple(p[-len(p)+1:])
	
def p_iteration_statement(p):
	'''iteration_statement : WHILE LPAREN expression RPAREN statement
							| DO statement WHILE LPAREN expression RPAREN SEMI
							| FOR LPAREN expression_statement expression_statement RPAREN statement
							| FOR LPAREN expression_statement expression_statement expression RPAREN statement
							| FOR LPAREN declaration expression_statement RPAREN statement
							| FOR LPAREN declaration expression_statement expression RPAREN statement
							 '''
	#print "iteration_statement"
	#p[0]=("iteration_statement",)+tuple(p[-len(p)+1:])

def p_jump_statement(p):
	'''jump_statement : GOTO IDENTIFIER SEMI 
						| CONTINUE SEMI
						| BREAK SEMI '''
	#print "jump_statement"
	#p[0]=("jump_statement",)+tuple(p[-len(p)+1:])

def p_jump_statement2(p):
	'''jump_statement : RETURN SEMI
						| RETURN expression SEMI '''
	#print "jump_statement"
	#p[0]=("jump_statement",)+tuple(p[-len(p)+1:])
	global returnSpecifier
	
	if(len(p) == 3):
		returnSpecifier = 'void'
		p[0] = {'TYPE':'void'}
	else:
		returnSpecifier = str(p[2]['TYPE'])
		p[0] = p[2]

def p_external_declaration(p):
	'''external_declaration : function_definition
							| declaration '''
	#print "external_declaration"
	#p[0]=("external_declaration",)+tuple(p[-len(p)+1:])

def p_function_definition(p):
	'''function_definition : declaration_specifiers declarator declaration_list compound_statement
							| declaration_specifiers declarator compound_statement '''
	#print "function_definition"
	#p[0]=("function_definition",)+tuple(p[-len(p)+1:])
	
	global FUNCTION_PROTOTYPE_DEFINITION
	global FUNCTION_PROTOTYPE_DECLARATION
	global functions
	global parametersymboltable
	global returnSpecifier

	#--------- return type check of a function
	#if(str(p[1]['TYPE']) != 'void'):
	#	if(returnSpecifier == ''):
	#		print "Error at line number", p.lineno(1) ,"return statement not found for function ", str(p[2][0])
	#		sys.exit()
	#	if(returnSpecifier != str(p[1]['TYPE'])):
	#		print "Error at line number", p.lineno(1) ,"invalid return statement for function ", str(p[2][0])
	#		sys.exit()
	#else:
	#	if(returnSpecifier != str(p[1]['TYPE'])):
	#		print "Error at line number", p.lineno(1) ,"invalid return statement for function ", str(p[2][0])
	#		sys.exit()

	returnSpecifier = 'void'
	#sys.call()
	if(len(p) == 5 ):
		p[0] = {'NODE_TYPE':'function_declaration', 'OUTPUT':p[1]['TYPE'], 'INPUT': p[2][0], 'IDENTIFIER': p[2][0],'partProgram': p[4]}
		flag = 0
		for func in FUNCTION_PROTOTYPE_DECLARATION :
				#print t[2]
				if(p[2][0] in func['NAME'] or p[2][0] == 'main'):
					flag=1
					func['partProgram'] = p[4]
					break
		if(flag != 1):
			print "function definition missing for ",p[2][0]
			currentfunction = {'Function Detail':p[0],'symboltable':parametersymboltable}
			functions = functions + [currentfunction]
			CURRENT_DECLARATION = [{"NAME":p[2][0],"INPUT":p[2][0],"OUTPUT":p[1]['TYPE']}]
			FUNCTION_PROTOTYPE_DEFINITION = FUNCTION_PROTOTYPE_DEFINITION + CURRENT_DECLARATION
			parametersymboltable = SymbolTable(-1)	

			
	elif(len(p) == 4 ):
		inp=[]
		if(len(p[2]) == 1):
			inp = ['void']
		else:
			for i in p[2][1]:
				inp=inp+[i[0]['TYPE']]
		p[0] = {'NODE_TYPE':'function_declaration', 'OUTPUT':p[1]['TYPE'], 'INPUT': inp, 'IDENTIFIER': p[2][0],'partProgram': p[3]}
		#print p[2][1][0]
		flag = 0
		for func in FUNCTION_PROTOTYPE_DECLARATION :
			if(p[2][0] in func['NAME']):
				if(str(func['INPUT']) != str(inp)):
					print "Error at line number", p.lineno(1) ,":function definition mismatch errors"
					sys.exit()
					#raise SyntaxError
		for func in FUNCTION_PROTOTYPE_DEFINITION :
				if(p[2][0] in func['NAME']):
					flag=1
					print "Error at line number", p.lineno(1) ,":function already defined"
					#raise SyntaxError
					break
		#print p[2][1][0]
		if(flag != 1):
			#print p[2][1][0]
			#print "function definition missing for ",p[2][0]
			currentfunction = {'Function Detail':p[0],'symboltable':parametersymboltable}
			#print p[2][1][0]
			functions = functions + [currentfunction]
			CURRENT_DECLARATION = [{"NAME":p[2][0],"INPUT":inp,"OUTPUT":p[1]['TYPE']}]
			#print len(p[2][1][0])
			FUNCTION_PROTOTYPE_DEFINITION = FUNCTION_PROTOTYPE_DEFINITION + CURRENT_DECLARATION
			parametersymboltable = SymbolTable(-1)
			
	


def p_declaration_list(p):
	'''declaration_list : declaration
						| declaration_list declaration '''
	#print "declaration_list"
	#p[0]=("declaration_list",)+tuple(p[-len(p)+1:])
	
	if(len(p)==2):
		p[0]=[p[1]]
	if(len(p) == 3):
		p[0]=p[1] + [p[3]]



def p_leftbrace(p):
	''' left_brace : LBRACE
					'''
	#p[0] = p[1]
	#print "-----Making NewSymbolTable---------"
	global currentSymbolTable
	currentSymbolTable = SymbolTable(currentSymbolTable)

def p_righttbrace(p):
	''' right_brace : RBRACE
					'''
	#p[0] = p[1]
	#print "--------EXITING CURRENT SYMBOL TABLE--------------"
	global currentSymbolTable
	currentSymbolTable = currentSymbolTable.father






########################### end


	
def p_error(p):
	global flag_for_error
	flag_for_error = 1

	if p is not None:
		print("error at line no:  %s :: %s"%((p.lineno),(p.value)))
		parser.errok()
	else:
		print("Unexpected end of input")


if __name__ == "__main__":
	import profile
	
	if len(sys.argv) < 2:
		print "No input file specified"
	else:
		parser = yacc.yacc()
		fo = open(str(sys.argv[1]), "r+")
		data = fo.read()
		fo.close()
		tree = yacc.parse(data,tracking=True)
		if tree is not None and flag_for_error == 0:
			#createParseTree.create_tree(tree,str(sys.argv[1]))
			print "Parse tree created : "+str(sys.argv[1])+"tree.svg"
			#os.system("eog "+str(sys.argv[1])+"tree.svg")
		#yacc.yacc(method='LALR',write_tables=False,debug=False)

		#profile.run("yacc.yacc(method='LALR')")
