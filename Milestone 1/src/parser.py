import sys
import os
import lexer
import ply.yacc as yacc
import createParseTree

from createParseTree import create_tree
from createParseTree import calc_tree
from createParseTree import tokenVal

tokens = lexer.tokens
flag_for_error = 0

def p_translation_unit(p):
	'''translation_unit : external_declaration
						| translation_unit external_declaration '''
	#print "translational_unit"
	p[0]=("translational_unit",)+tuple(p[-len(p)+1:])

def p_primary_expression(p):
	'''primary_expression : IDENTIFIER
							| constant
							| string
							| LPAREN expression RPAREN
							| generic_selection '''
	#print "primary_expression"
	p[0]=("primary_expression",)+tuple(p[-len(p)+1:])

def p_constant(p):
	'''constant : I_CONSTANT
				| F_CONSTANT
				| CCONST '''
	#print "constant"
	p[0]=("primary_expression",)+tuple(p[-len(p)+1:])
	
def p_enumeration_constant(p):
	'''enumeration_constant : IDENTIFIER'''
	#print "enumeration_constant"
	p[0]=("enumeration_constant",)+tuple(p[-len(p)+1:])

def p_string(p):
	'''string : STRINGLITERAL
				| FUNC_NAME '''
	#print "string"
	p[0]=("string",)+tuple(p[-len(p)+1:])
	
def p_generic_selection(p):
	'''generic_selection : GENERIC LPAREN assignment_expression COMMA generic_assoc_list RPAREN '''
	#print "generic_selection"
	p[0]=("generic_selection",)+tuple(p[-len(p)+1:])
	
def p_generic_assoc_list(p):
	'''generic_assoc_list : generic_association
							| generic_assoc_list COMMA generic_association '''
	#print "generic_assoc_list"
	p[0]=("generic_assoc_list",)+tuple(p[-len(p)+1:])
	
def p_generic_association(p):
	'''generic_association : type_name COLON assignment_expression
							| DEFAULT COLON assignment_expression '''
	#print "generic_association"
	p[0]=("generic_association",)+tuple(p[-len(p)+1:])
		
def p_postfix_expression(p):
	'''postfix_expression : primary_expression
							| postfix_expression LBRACKET expression RBRACKET
							| postfix_expression LPAREN RPAREN
							| postfix_expression LPAREN argument_expression_list RPAREN
							| postfix_expression PERIOD IDENTIFIER
							| postfix_expression PTR_OP IDENTIFIER
							| postfix_expression INC_OP
							| postfix_expression DEC_OP
							| LPAREN type_name RPAREN LBRACE initializer_list RBRACE
							| LPAREN type_name RPAREN LBRACE initializer_list COMMA RBRACE '''
	#print "postfix_expresssion"
	p[0]=("postfix_expresssion",)+tuple(p[-len(p)+1:])
		
def p_argument_expression_list(p):
	'''argument_expression_list : assignment_expression
								| argument_expression_list COMMA assignment_expression '''
	#print "argument_expression_list"
	p[0]=("argument_expression_list",)+tuple(p[-len(p)+1:])
		
def p_unary_expression(p):
	'''unary_expression : postfix_expression
						| INC_OP unary_expression
						| DEC_OP unary_expression
						| unary_operator cast_expression
						| SIZEOF unary_expression
						| SIZEOF LPAREN type_name RPAREN
						| ALIGNOF LPAREN type_name RPAREN '''
	#print "unary_expression"
	p[0]=("unary_expression",)+tuple(p[-len(p)+1:])
		
def p_unary_operator(p):
	'''unary_operator : AND_OP
						| TIMES
						| PLUS
						| MINUS
						| NOT_OP
						| LNOT '''     #changetoken
	#print "unary_operator"
	p[0]=("unary_operator",)+tuple(p[-len(p)+1:])
		
def p_cast_expression(p):
	'''cast_expression : unary_expression
						| LPAREN type_name RPAREN cast_expression '''
	#print "cast_expression"
	p[0]=("cast_expression",)+tuple(p[-len(p)+1:])
		
def p_multiplicative_expression(p):
	'''multiplicative_expression : cast_expression
								 | multiplicative_expression TIMES cast_expression
								 | multiplicative_expression DIVIDE cast_expression 
								 | multiplicative_expression MOD cast_expression '''
	#print "multiplicative_expression"
	p[0]=("multiplicative_expression",)+tuple(p[-len(p)+1:])
		
def p_additive_expression(p):
	'''additive_expression : multiplicative_expression
							| additive_expression PLUS multiplicative_expression
							| additive_expression MINUS multiplicative_expression '''
	#print "additive_expression"
	p[0]=("additive_expression",)+tuple(p[-len(p)+1:])
		
def p_shift_expression(p):
	'''shift_expression : additive_expression
						| shift_expression LEFT_OP additive_expression
						| shift_expression RIGHT_OP additive_expression '''
	#print "shift_expression"
	p[0]=("shift_expression",)+tuple(p[-len(p)+1:])
	
def p_relational_expression(p):
	'''relational_expression : shift_expression
								| relational_expression LT_OP shift_expression
								| relational_expression GT_OP shift_expression
								| relational_expression LE_OP shift_expression
								| relational_expression GE_OP shift_expression '''
	#print "relational_expression"
	p[0]=("relational_expression",)+tuple(p[-len(p)+1:])
		
def p_equality_expression(p):
	'''equality_expression : relational_expression
	 						| equality_expression EQ_OP relational_expression
	 						| equality_expression NE_OP relational_expression '''
	#print "equality_expression"
	p[0]=("equality_expression",)+tuple(p[-len(p)+1:])
	
def p_and_expression(p):
	'''and_expression : equality_expression
						| and_expression AND_OP equality_expression '''
	#print "and_expression"
	p[0]=("and_expression",)+tuple(p[-len(p)+1:])
	
def p_exclusive_or_expression(p):
	'''exclusive_or_expression : and_expression
								| exclusive_or_expression XOR and_expression '''
	#print "exclusive_or_expression"
	p[0]=("exclusive_or_expression",)+tuple(p[-len(p)+1:])
	
def p_inclusive_or_expression(p):
	'''inclusive_or_expression : exclusive_or_expression
								| inclusive_or_expression OR_OP exclusive_or_expression '''
	#print "inclusive_or_expression"
	p[0]=("inclusive_or_expression",)+tuple(p[-len(p)+1:])
	
def p_logical_and_expression(p):
	'''logical_and_expression : inclusive_or_expression
								| logical_and_expression LAND inclusive_or_expression '''
	#print "logical_and_expression"
	p[0]=("logical_and_expression",)+tuple(p[-len(p)+1:])
	
def p_logical_or_expression(p):
	'''logical_or_expression : logical_and_expression
								| logical_or_expression LOR logical_and_expression '''
	#print "logical_or_expression"
	p[0]=("logical_or_expression",)+tuple(p[-len(p)+1:])
		
def p_conditional_expression(p):
	'''conditional_expression : logical_or_expression
								| logical_or_expression CONDOP expression COLON conditional_expression '''
	#print "conditional_expression"
	p[0]=("conditional_expression",)+tuple(p[-len(p)+1:])
		
def p_assignment_expression(p):
	'''assignment_expression : conditional_expression
								| unary_expression assignment_operator assignment_expression '''
	#print "assignment_expression"
	p[0]=("assignment_expression",)+tuple(p[-len(p)+1:])
	
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
	p[0]=("assignment_operator",)+tuple(p[-len(p)+1:])
	
def p_expression(p):
	'''expression : assignment_expression
					| expression COMMA assignment_expression '''
	#print "expression"
	p[0]=("expression",)+tuple(p[-len(p)+1:])
	
def p_constant_expression(p):
	'''constant_expression : conditional_expression'''
	#print "constant_expression"
	p[0]=("constant_expression",)+tuple(p[-len(p)+1:])
	
def p_declaration(p):
	'''declaration : declaration_specifiers SEMI
					| declaration_specifiers init_declarator_list SEMI
					| static_assert_declaration '''
	#print "declaration"
	p[0]=("declaration",)+tuple(p[-len(p)+1:])
		
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
	p[0]=("declaration_specifiers",)+tuple(p[-len(p)+1:])
	
def p_init_declarator_list(p):
	'''init_declarator_list : init_declarator
							| init_declarator_list COMMA init_declarator '''
	#print "init_declarator_list"
	p[0]=("init_declarator_list",)+tuple(p[-len(p)+1:])
	
def p_init_declarator(p):
	'''init_declarator : declarator EQUALS initializer
						| declarator '''
	#print "init_declarator"
	p[0]=("init_declarator",)+tuple(p[-len(p)+1:])
		
def p_storage_class_specifier(p):
	'''storage_class_specifier : TYPEDEF
								| EXTERN
								| STATIC
								| THREAD_LOCAL
								| AUTO
								| REGISTER '''
	#print "storage_class_specifier"
	p[0]=("storage_class_specifier",)+tuple(p[-len(p)+1:])
	
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
						| struct_or_union_specifier
						| enum_specifier
						| TYPEID '''
	#print "type_specifier"
	p[0]=("type_specifier",)+tuple(p[-len(p)+1:])
		
def p_struct_or_union_specifier(p):
	'''struct_or_union_specifier : struct_or_union LBRACE struct_declaration_list RBRACE
								| struct_or_union IDENTIFIER LBRACE struct_declaration_list RBRACE
								| struct_or_union IDENTIFIER '''
	#print "struct_or_union_specifier"
	p[0]=("struct_or_union_specifier",)+tuple(p[-len(p)+1:])
	
def p_struct_or_union(p):
	'''struct_or_union : STRUCT
						| UNION '''
	#print "struct_or_union"
	p[0]=("struct_or_union",)+tuple(p[-len(p)+1:])
	
def p_struct_declaration_list(p):
	'''struct_declaration_list : struct_declaration
								| struct_declaration_list struct_declaration '''
	#print "struct_declaration_list"
	p[0]=("struct_declaration_list",)+tuple(p[-len(p)+1:])
	
def p_struct_declaration(p):
	'''struct_declaration : specifier_qualifier_list SEMI 
							| specifier_qualifier_list struct_declarator_list SEMI
							| static_assert_declaration '''
	#print "struct_declaration"
	p[0]=("struct_declaration",)+tuple(p[-len(p)+1:])

def p_specifier_qualifier_list(p):
	'''specifier_qualifier_list : type_specifier specifier_qualifier_list
								| type_specifier
								| type_qualifier specifier_qualifier_list
								| type_qualifier '''
	#print "specifier_qualifier_list"
	p[0]=("specifier_qualifier_list",)+tuple(p[-len(p)+1:])
	
def p_struct_declarator_list(p):
	'''struct_declarator_list : struct_declarator
								| struct_declarator_list COMMA struct_declarator '''
	#print "struct_declarator_list"
	p[0]=("struct_declarator_list",)+tuple(p[-len(p)+1:])                       #changetoken
	
def p_struct_declarator(p):
	'''struct_declarator : COLON constant_expression
							| declarator COLON constant_expression
							| declarator '''
	#print "struct_declarator"
	p[0]=("struct_declarator",)+tuple(p[-len(p)+1:])                        #changetoken
	
def p_enum_specifier(p):
	'''enum_specifier : ENUM LBRACE enumerator_list RBRACE
						| ENUM LBRACE enumerator_list COMMA RBRACE
						| ENUM IDENTIFIER LBRACE enumerator_list RBRACE
						| ENUM IDENTIFIER LBRACE enumerator_list COMMA RBRACE
						| ENUM IDENTIFIER '''
	#print "enum_specifier"
	p[0]=("enum_specifier",)+tuple(p[-len(p)+1:])                        #changetoken
	
def p_enumerator_list(p):
	'''enumerator_list : enumerator
						| enumerator_list COMMA enumerator '''
	#print "enumerator_list"
	p[0]=("enumerator_list",)+tuple(p[-len(p)+1:])                        #changetoken
	
def p_enumerator(p):
	'''enumerator : enumeration_constant EQUALS constant_expression
					| enumeration_constant '''
	#print "enumerator"
	p[0]=("enumerator",)+tuple(p[-len(p)+1:])                      
	
def p_type_qualifier(p):
	'''type_qualifier : CONST
						| RESTRICT
						| VOLATILE
						'''
	#print "type_qualifier"
	p[0]=("type_qualifier",)+tuple(p[-len(p)+1:])
	
def p_function_specifier(p):
	'''function_specifier : INLINE
							| NORETURN '''
	#print "function_specifier"
	p[0]=("function_specifier",)+tuple(p[-len(p)+1:])
	
def p_alignment_specifier(p):
	'''alignment_specifier : ALIGNAS LPAREN type_name RPAREN 
							| ALIGNAS LPAREN constant_expression RPAREN '''
	#print "alignment_specifier"
	p[0]=("alignment_specifier",)+tuple(p[-len(p)+1:])
	
def p_declarator(p):
	'''declarator : pointer direct_declarator
					| direct_declarator '''
	#print "declarator"
	p[0]=("declarator",)+tuple(p[-len(p)+1:])

def p_direct_declarator(p):
	'''direct_declarator : IDENTIFIER
							| LPAREN declarator RPAREN
							| direct_declarator LBRACKET RBRACKET
							| direct_declarator LBRACKET TIMES RBRACKET
							| direct_declarator LBRACKET STATIC type_qualifier_list assignment_expression RBRACKET
							| direct_declarator LBRACKET STATIC assignment_expression RBRACKET
							| direct_declarator LBRACKET type_qualifier_list TIMES RBRACKET
							| direct_declarator LBRACKET type_qualifier_list STATIC assignment_expression RBRACKET
							| direct_declarator LBRACKET type_qualifier_list assignment_expression RBRACKET
							| direct_declarator LBRACKET type_qualifier_list RBRACKET
							| direct_declarator LBRACKET assignment_expression RBRACKET
							| direct_declarator LPAREN parameter_type_list RPAREN
							| direct_declarator LPAREN RPAREN
							| direct_declarator LPAREN identifier_list RPAREN '''
	#print "direct_declarator"
	p[0]=("direct_declarator",)+tuple(p[-len(p)+1:])
	
def p_pointer(p):
	'''pointer : TIMES type_qualifier_list pointer
				| TIMES type_qualifier_list 
				| TIMES pointer
				| TIMES '''
	#print "pointer"
	p[0]=("pointer",)+tuple(p[-len(p)+1:])
	
def p_type_qualifier_list(p):
	'''type_qualifier_list : type_qualifier
							| type_qualifier_list type_qualifier '''
	#print "type_qualifier_list"
	p[0]=("type_qualifier_list",)+tuple(p[-len(p)+1:])
	
def p_parameter_type_list(p):
	'''parameter_type_list : parameter_list COMMA ELLIPSIS
							| parameter_list '''
	#print "parameter_type_list"
	p[0]=("parameter_type_list",)+tuple(p[-len(p)+1:])
	
def p_parameter_list(p):
	'''parameter_list : parameter_declaration
						| parameter_list COMMA parameter_declaration '''
	#print "parameter_list"
	p[0]=("parameter_list",)+tuple(p[-len(p)+1:])
	
def p_parameter_declaration(p):
	'''parameter_declaration : declaration_specifiers declarator
								| declaration_specifiers abstract_declarator
								| declaration_specifiers '''
	#print "parameter_declaration"
	p[0]=("parameter_declaration",)+tuple(p[-len(p)+1:])
	
def p_identifier_list(p):
	'''identifier_list : IDENTIFIER
						| identifier_list COMMA IDENTIFIER '''
	#print "identifier_list"
	p[0]=("identifier_list",)+tuple(p[-len(p)+1:])
	
def p_type_name(p):
	'''type_name : specifier_qualifier_list abstract_declarator
					| specifier_qualifier_list '''
	#print "type_name"
	p[0]=("type_name",)+tuple(p[-len(p)+1:])
	
def p_abstract_declarator(p):
	'''abstract_declarator : pointer direct_abstract_declarator
							| pointer
							| direct_abstract_declarator '''
	#print "abstarct_declarator"
	p[0]=("abstarct_declarator",)+tuple(p[-len(p)+1:])
	
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
	p[0]=("direct_abstract_declarator",)+tuple(p[-len(p)+1:])
	
def p_initializer(p):
	'''initializer : LBRACE initializer_list RBRACE
					| LBRACE initializer_list COMMA RBRACE 
					| assignment_expression '''
	#print "initializer"
	p[0]=("initializer",)+tuple(p[-len(p)+1:])
	
def p_initializer_list(p):
	'''initializer_list : designation initializer
						| initializer
						| initializer_list COMMA designation initializer
						| initializer_list COMMA initializer
						'''
	#print "initializer_list"
	p[0]=("initializer_list",)+tuple(p[-len(p)+1:])
	
def p_designation(p):
	'''designation : designator_list EQUALS '''
	#print "designation"
	p[0]=("designation",)+tuple(p[-len(p)+1:])
	
def p_designator_list(p):
	'''designator_list : designator
						| designator_list designator '''
	#print "designator_list"
	p[0]=("designator_list",)+tuple(p[-len(p)+1:])
	
def p_designator(p):
	'''designator : LBRACKET constant_expression RBRACKET 
					| PERIOD IDENTIFIER '''
	#print "designator"
	p[0]=("designator",)+tuple(p[-len(p)+1:])
	
def p_static_assert_declaration(p):
	'''static_assert_declaration : STATIC_ASSERT LPAREN constant_expression COMMA STRINGLITERAL RPAREN SEMI '''
	#print "static_assert_declaration"
	p[0]=("static_assert_declaration",)+tuple(p[-len(p)+1:])
	
def p_statement(p):
	'''statement : labeled_statement
					| compound_statement
					| expression_statement
					| selection_statement
					| iteration_statement
					| jump_statement '''
	#print "statement"
	p[0]=("statement",)+tuple(p[-len(p)+1:])
	
def p_labeled_statement(p):
	'''labeled_statement : IDENTIFIER COLON statement
						| CASE constant_expression COLON statement
						| DEFAULT COLON statement
						 '''
	#print "labeled_statement"
	p[0]=("labeled_statement",)+tuple(p[-len(p)+1:])
	
def p_compound_statement(p):
	'''compound_statement : LBRACE RBRACE 
							| LBRACE block_item_list RBRACE '''
	#print "compound_statement"
	p[0]=("compound_statement",)+tuple(p[-len(p)+1:])
	
def p_block_item_list(p):
	'''block_item_list : block_item
						| block_item_list block_item '''
	#print "block_item_list"
	p[0]=("block_item_list",)+tuple(p[-len(p)+1:])
	
def p_block_item(p):
	'''block_item : declaration
					| statement '''
	#print "block_item"
	p[0]=("block_item",)+tuple(p[-len(p)+1:])
	
def p_expression_statement(p):
	'''expression_statement : SEMI 
							| expression SEMI  '''
	#print "expression_statement"
	p[0]=("expression_statement",)+tuple(p[-len(p)+1:])

def p_selection_statement(p):
	'''selection_statement : IF LPAREN expression RPAREN statement ELSE statement
							| IF LPAREN expression RPAREN statement  
							| SWITCH LPAREN expression RPAREN statement '''
	#print "selection_statement"
	p[0]=("selection_statement",)+tuple(p[-len(p)+1:])
	
def p_iteration_statement(p):
	'''iteration_statement : WHILE LPAREN expression RPAREN statement
							| DO statement WHILE LPAREN expression RPAREN SEMI
							| FOR LPAREN expression_statement expression_statement RPAREN statement
							| FOR LPAREN expression_statement expression_statement expression RPAREN statement
							| FOR LPAREN declaration expression_statement RPAREN statement
							| FOR LPAREN declaration expression_statement expression RPAREN statement
							 '''
	#print "iteration_statement"
	p[0]=("iteration_statement",)+tuple(p[-len(p)+1:])

def p_jump_statement(p):
	'''jump_statement : GOTO IDENTIFIER SEMI 
						| CONTINUE SEMI
						| BREAK SEMI
						| RETURN SEMI
						| RETURN expression SEMI '''
	#print "jump_statement"
	p[0]=("jump_statement",)+tuple(p[-len(p)+1:])
	
def p_external_declaration(p):
	'''external_declaration : function_definition
							| declaration '''
	#print "external_declaration"
	p[0]=("external_declaration",)+tuple(p[-len(p)+1:])

def p_function_definition(p):
	'''function_definition : declaration_specifiers declarator declaration_list compound_statement
							| declaration_specifiers declarator compound_statement '''
	#print "function_definition"
	p[0]=("function_definition",)+tuple(p[-len(p)+1:])

def p_declaration_list(p):
	'''declaration_list : declaration
						| declaration_list declaration '''
	#print "declaration_list"
	p[0]=("declaration_list",)+tuple(p[-len(p)+1:])
	
	
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
		tree = yacc.parse(data)
		if tree is not None and flag_for_error == 0:
			createParseTree.create_tree(tree,str(sys.argv[1]))
			print "Parse tree created : "+str(sys.argv[1])+"tree.svg"
			os.system("eog "+str(sys.argv[1])+"tree.svg")
		#yacc.yacc(method='LALR',write_tables=False,debug=False)

		#profile.run("yacc.yacc(method='LALR')")
