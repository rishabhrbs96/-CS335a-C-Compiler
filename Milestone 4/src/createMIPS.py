from SymbolTable import *

data_section = []
text_section = []
global_text = []
global if_begin

addressDescriptor = {}
registerDescriptor = { '$t0' : None, '$t1' : None, '$t2' : None, '$t3' : None, '$t4' : None, '$t5' : None,  '$t6' : None, '$t7' : None, '$t8' : None, '$t9' : None, '$s0' : None, '$s1' : None, '$s2' : None, '$s3' : None, '$s4' : None }
freeRegisters = ['$s4','$s3','$s2','$s1','$s0','$t9', '$t8', '$t7', '$t6', '$t5', '$t4', '$t3', '$t2', '$t1', '$t0']
busyRegisters = []

declaredVars = []
global currentSymbolTable
global symbolTableStack
symbolTableStack = []
global tempVarCounter

def convName(var):
	global currentSymbolTable
	tmp = currentSymbolTable.lookup(var)
	if(tmp == False):
		return ('VAR_'+currentSymbolTable.tableName+"_"+var)
	else:
		return ('VAR_'+tmp['scope']+"_"+var)
				
def addIns(ins):
	global if_begin
	global text_section
	global global_text

	if(if_begin == 1):
		text_section += [ins]
	else:
		global_text += [ins]

def isVar(var):
	#global currentSymbolTable
	#global tempVarCounter
	#if(currentSymbolTable.lookup(var) == False):
	#	if(var[0:2] == 't_' and int(var[2:]) <= tempVarCounter):
	#		return True
	#	return False
	#return True
	return (not var.isdigit())

def getReg(var):
	global registerDescriptor
	global freeRegisters
	global busyRegisters
	global addressDescriptor
	global text_section
	global declaredVars

	register = ""
	if(var in registerDescriptor.values()):
		register = addressDescriptor[var]
	else:
		if(len(freeRegisters) == 0):

			pass		
		else:
			register = freeRegisters.pop()
			addressDescriptor[var] = register
			busyRegisters.append(register)
			registerDescriptor[register] = var
			if(var in declaredVars):
				addIns("\tlw\t"+register+",\t"+var)
	return register

def data_size(data_type):
	if(data_type=="float"):
		return 4
	if(data_type == "int"):
		return 4;
	if(data_type == "double"):
		return 8
	if(data_type == "char"):
		return 1

def create_mips(code,symboltable,tempVarcounter):
	global data_section
	global text_section
	global declaredVars
	global currentSymbolTable
	global tempVarCounter
	global global_text
	global if_begin

	tempVarCounter = tempVarcounter
	currentSymbolTable = symboltable
	if_main = 0
	if_begin = 0
	print "----------- Three Address Code -----------\n"
	for line in code:
		print line
		if(line != []):
			if(line[0] == 'ARRDECLARATION'):
				if(int(line[3])==2):
					tot_mem=(int(line[4])*int(line[5]))*data_size(line[1])
					#check the data type here of the array
					data_section += ["\tVAR_"+line[2]+":\t.space\t"+str(tot_mem)]
				if(int(line[3])==1):
					tot_mem =(int(line[4]))*data_size(line[1])
					data_section += ["\tVAR_"+line[2]+":\t.space\t"+str(tot_mem)]
					#check the data type here of the array
			elif(line[0] == 'GETARRAY'):
				if(line[3] == '1'):
					if(line[4].isdigit()):
						offset=4*int(line[4])
						
						offset_register = getReg(convName(line[1]))
						addIns("\taddi\t"+offset_register+",\t$zero,\t"+str(offset))
						addIns("\tlw\t"+offset_register+",\tVAR_"+line[2]+"("+offset_register+")")
						
					elif(isVar(line[4])):
						register=getReg(convName(line[4]))
						offset_register = getReg(convName(line[1]))
						addIns("\tmul\t"+offset_register+",\t"+register+",\t4")
						addIns("\tlw\t"+offset_register+",\tVAR_"+line[2]+"("+offset_register+")")
						
				elif(line[3] == '2'):  #change the the offset as the product of current row and the total number of columns 
					#need the dimension of the 2-d array
					arrdet = currentSymbolTable.lookup(line[2])
					col = arrdet['dimension'][1]

					if(line[4].isdigit() and line[5].isdigit()):
						#offset = data_size('int')*int(line[4])*int(line[5])
						#offset_register = freeRegisters.pop()
						offset = (int(line[4])*col + int(line[5]))*data_size(arrdet['output'])
						offset_register = getReg(convName(line[1]))
						addIns("\taddi\t"+offset_register+",\t$zero,\t"+str(offset))
						addIns("\tlw\t"+offset_register+",\tVAR_"+line[2]+"("+offset_register+")")
						
					elif(isVar(line[4]) and line[5].isdigit()):
						reg_var= getReg(convName(line[4]))
						offset_register = getReg(convName(line[1]))
						addIns("\tmul\t"+offset_register+",\t"+reg_var+",\t"+str(col))
						addIns("\taddi\t"+offset_register+",\t"+offset_register+",\t"+line[5])
						addIns("\tmul\t"+offset_register+",\t"+offset_register+",\t"+str(data_size(arrdet['output'])))
						addIns("\tlw\t"+offset_register+",\tVAR_"+line[2]+"("+offset_register+")")

					elif(line[4].isdigit() and isVar(line[5])):
						reg_var= getReg(convName(line[5]))
						offset_register = getReg(convName(line[1]))
						addIns("\taddi\t"+offset_register+",\t$zero,\t"+str(int(line[4])*col))
						addIns("\tadd\t"+offset_register+",\t"+offset_register+",\t"+reg_var)
						addIns("\tmul\t"+offset_register+",\t"+offset_register+",\t"+str(data_size('int')))
						addIns("\tlw\t"+offset_register+",\tVAR_"+line[2]+"("+offset_register+")")
					
					elif(isVar(line[4]) and isVar(line[5])):
						reg_var1 = getReg(convName(line[4]))
						reg_var2 = getReg(convName(line[5]))
						offset_register = getReg(convName(line[1]))
						addIns("\tmul\t"+offset_register+",\t"+reg_var1+",\t"+str(col))
						addIns("\tadd\t"+offset_register+",\t"+offset_register+",\t"+reg_var2)
						addIns("\tmul\t"+offset_register+",\t"+offset_register+",\t"+str(data_size('int')))
						addIns("\tlw\t"+offset_register+",\tVAR_"+line[2]+"("+offset_register+")")

			elif(line[0]=='PUTARRAY'):
				if(line[3]=='1'):
					if(line[4].isdigit()):
						offset = data_size('int')*int(line[4])
						value_register = getReg(convName(line[1]))
						offset_register = freeRegisters.pop()
						addIns("\taddi\t"+offset_register+",\t$zero,\t"+str(offset))
						addIns("\tsw\t"+value_register+",\tVAR_"+line[2]+"("+offset_register+")")
						freeRegisters.append(offset_register)
					
					elif(isVar(line[4])):
						index_register = getReg(convName(line[4]))
						value_register = getReg(convName(line[1]))
						offset_register = freeRegisters.pop()
						addIns("\tmul\t"+offset_register+",\t"+index_register+",\t"+str(data_size('int')))
						addIns("\tsw\t"+value_register+",\tVAR_"+line[2]+"("+offset_register+")")
						freeRegisters.append(offset_register)
				
				elif(line[3]=='2'):   #change the offset as the product of the current row and total numnber of colums 
						arrdet = currentSymbolTable.lookup(line[2])
						col = arrdet['dimension'][1]
						if(line[4].isdigit() and line[5].isdigit()):
							#offset=data_size('int')*int(line[4])*int(line[5])
							offset = (int(line[4])*col + int(line[5]))*data_size(arrdet['output'])
							value_register = getReg(convName(line[1]))
							offset_register = freeRegisters.pop()
							addIns("\taddi\t"+offset_register+",\t$zero,\t"+str(offset))
							addIns("\tsw\t"+value_register+",\tVAR_"+line[2]+"("+offset_register+")")
							freeRegisters.append(offset_register)

						if(line[4].isdigit() and isVar(line[5])):
							index_register = getReg(convName(line[5]))
							offset_register = freeRegisters.pop()
							addIns("\taddi\t"+offset_register+",\t$zero,\t"+str(int(line[4])*col))
							addIns("\tadd\t"+offset_register+",\t"+offset_register+",\t"+index_register)
							addIns("\tmul\t"+offset_register+",\t"+offset_register+",\t"+str(data_size(arrdet['output'])))
							value_register = getReg(convName(line[1]))
							addIns("\tsw\t"+value_register+",\tVAR_"+line[2]+"("+offset_register+")")
							freeRegisters.append(offset_register)
						
						if(isVar(line[4]) and line[5].isdigit()):
							index_register = getReg(convName(line[4]))
							offset_register = freeRegisters.pop()
							addIns("\tmul\t"+offset_register+",\t"+index_register+",\t"+str(col))
							addIns("\taddi\t"+offset_register+",\t"+offset_register+",\t"+line[5])
							addIns("\tmul\t"+offset_register+",\t"+offset_register+",\t"+str(data_size(arrdet['output'])))
							value_register = getReg(convName(line[1]))
							addIns("\tsw\t"+value_register+",\tVAR_"+line[2]+"("+offset_register+")")
							freeRegisters.append(offset_register)
						
						if(isVar(line[4]) and isVar(line[5])):
							index_register1 = getReg(convName(line[4]))
							index_register2 = getReg(convName(line[5]))
							offset_register = freeRegisters.pop()
							addIns("\tmul\t"+offset_register+",\t"+index_register1+",\t"+str(col))
							addIns("\tadd\t"+offset_register+",\t"+offset_register+",\t"+index_register2)
							addIns("\tmul\t"+offset_register+",\t"+offset_register+",\t"+str(data_size(arrdet['output'])))
							value_register = getReg(convName(line[1]))
							addIns("\tsw\t"+value_register+",\tVAR_"+line[2]+"("+offset_register+")")
							freeRegisters.append(offset_register)

			elif(line[0] == "!"):
				reg1 = getReg(convName(line[1]))
				reg2 = getReg(convName(line[2]))
				addIns("\tnot\t"+reg1+",\t"+reg2)

			elif(line[0]=='&&'):
				if(isVar(line[2]) and isVar(line[3])):
					reg1=getReg(convName(line[1]))
					reg2=getReg(convName(line[2]))
					reg3=getReg(convName(line[3]))
					addIns("\tand\t"+reg1+",\t"+reg2+",\t"+reg3)

				elif(isVar(line[2]) and line[3].isdigit()):
					reg1=getReg(convName(line[1]))
					reg2=getReg(convName(line[2]))
					addIns("\tandi\t"+reg1+",\t"+reg2+",\t"+line[3])

				elif(isVar(line[3]) and line[2].isdigit()):
					reg1=getReg(convName(line[1]))
					reg2=getReg(convName(line[3]))
					addIns("\tandi\t"+reg1+",\t"+reg2+",\t"+line[2])

			elif(line[0]=='||'):
				if(isVar(line[2]) and isVar(line[3])):
					reg1=getReg(convName(line[1]))
					reg2=getReg(convName(line[2]))
					reg3=getReg(convName(line[3]))
					addIns("\tor\t"+reg1+",\t"+reg2+",\t"+reg3)

				elif(isVar(line[2]) and line[3].isdigit()):
					reg1=getReg(convName(line[1]))
					reg2=getReg(convName(line[2]))
					addIns("\tori\t"+reg1+",\t"+reg2+",\t"+line[3])

				elif(isVar(line[3]) and line[2].isdigit()):
					reg1=getReg(convName(line[1]))
					reg2=getReg(convName(line[3]))
					addIns("\tori\t"+reg1+",\t"+reg2+",\t"+line[2])			

			elif(line[0]=='FCALL'):
				if(len(line)==2):
					#function that doesn't return 
					pass
				elif(len(line)==3):
					#store_val = getReg("FUN_"+line[1])
					#function that returns value
					pass
			elif(line[0] == 'BEGINFUCTION'):
				if_begin = 1
				symbolTableStack.append(currentSymbolTable)
				currentSymbolTable = currentSymbolTable.childList[line[2]]
				if(line[2]=="main"):
					if_main =1
				else:
					if_main=0
					addIns("\taddi\t$sp,\t$sp,\t-4")
					addIns("\tsw\t$ra,\t0($sp)")
				addIns(line[2]+':')
				pass
			elif(line[0] == 'ENDFUNCTION'):
				currentSymbolTable = symbolTableStack.pop()
				if(if_main==1):
					if_main=1
					addIns("\tli\t$v0,\t10")
					addIns("\tsyscall")
				else:
					addIns("\tlw\t$ra,\t0($sp)")
					addIns("\taddi\t$sp,\t$sp,\t4")
					addIns("\tjr\t$ra")
				if_begin = 0

			elif(line[0] == 'VARDECLARATION'):
				data_size2 = 0
				if(line[1]=='void'): 
					data_size2=0
				elif(line[1]=='char'): 
					data_size2=1
				elif(line[1]=='int'): 
					data_size2=4
					tmp = currentSymbolTable.lookup(line[2])
					data_section += ['\tVAR_'+tmp['scope']+"_"+line[2]+':\t.word\t0']
					declaredVars.append('VAR_'+tmp['scope']+"_"+line[2])
				elif(line[1]=='float'): 
					data_size2=4
				elif(line[1]=='double'): 
					data_size2s=8
				else:
					pass
				#data_section += ['\tVAR_'+line[2]+'\t.space\t'+str(data_size)]
				pass
			elif(line[0] == 'LABEL'):
				addIns(line[1]+':')
				pass
			elif(line[0] == 'GOTO'):
				addIns("\tb\t"+line[1])
				pass
			elif(line[0] == 'IF'):
				if(line[2] == "=="):
					register = line[1]
					register3 = line[3]
					if(isVar(line[1])):
						register = getReg(convName(line[1]))
					if(isVar(line[3])):
						register3 = getReg(convName(line[3]))
					addIns("\tbeq\t"+register+",\t"+register3+",\t"+line[5])
				elif (line[2] == "<"):
					register = line[1]
					register3 = line[3]
					if(isVar(line[1])):
						register = getReg(convName(line[1]))
					if(isVar(line[3])):
						register3 = getReg(convName(line[3]))
					addIns("\tblt\t"+register+",\t"+register3+",\t"+line[5])
				elif (line[2] == ">"):
					register = line[1]
					register3 = line[3]
					if(isVar(line[1])):
						register = getReg(convName(line[1]))
					if(isVar(line[3])):
						register3 = getReg(convName(line[3]))
					addIns("\tbgt\t"+register+",\t"+register3+",\t"+line[5])
				elif (line[2] == "<="):
					register = line[1]
					register3 = line[3]
					if(isVar(line[1])):
						register = getReg(convName(line[1]))
					if(isVar(line[3])):
						register3 = getReg(convName(line[3]))
					addIns("\tble\t"+register+",\t"+register3+",\t"+line[5])
				elif (line[2] == ">="):
					register = line[1]
					register3 = line[3]
					if(isVar(line[1])):
						register = getReg(convName(line[1]))
					if(isVar(line[3])):
						register3 = getReg(convName(line[3]))
					addIns("\tbge\t"+register+",\t"+register3+",\t"+line[5])
				else:
					pass
				pass
			elif(line[0] == 'PRINTINT'):
				addIns("\tli\t$v0,\t1")
				if(isVar(line[1])):
					register = getReg(convName(line[1]))
					addIns("\tmove\t$a0,\t"+register)
				else:
					addIns("\tli\t$a0,\t"+line[1])
				addIns("\tsyscall")
				pass
			elif(line[0] == '+'):
				register = getReg(convName(line[1]))
				#register = getReg(convName(tmp['scope']+"_"+line[1])
				register2 = line[2]
				register3 = line[3]
				if(isVar(line[2])):
					register2 = getReg(convName(line[2]))
				if(isVar(line[3])):
					register3 = getReg(convName(line[3]))
				addIns("\tadd\t"+register+",\t"+register2+",\t"+register3)
				pass
			elif(line[0] == '-'):
				register = getReg(convName(line[1]))
				register2 = line[2]
				register3 = line[3]
				if(isVar(line[2])):
					register2 = getReg(convName(line[2]))
				if(isVar(line[3])):
					register3 = getReg(convName(line[3]))
				addIns("\tsub\t"+register+",\t"+register2+",\t"+register3)
				pass
			elif(line[0] == '*'):
				register = getReg(convName(line[1]))
				register2 = line[2]
				register3 = line[3]
				if(isVar(line[2])):
					register2 = getReg(convName(line[2]))
				if(isVar(line[3])):
					register3 = getReg(convName(line[3]))
				addIns("\tmul\t"+register+",\t"+register2+",\t"+register3)
				pass
			elif(line[0] == '/'):
				register = getReg(convName(line[1]))
				register2 = line[2]
				register3 = line[3]
				if(isVar(line[2])):
					register2 = getReg(convName(line[2]))
				if(isVar(line[3])):
					register3 = getReg(convName(line[3]))
				addIns("\tdiv\t"+register+",\t"+register2+",\t"+register3)
				pass
			elif(line[0] == '='):
				register = getReg(convName(line[1]))
				if(isVar(line[2])):
					register2 = getReg(convName(line[2]))
					addIns("\tmove\t"+register+",\t"+register2)
				else:
					addIns("\tli\t"+register+",\t"+line[2])
				pass
			elif(line[0] == '++'):
				register = getReg(convName(line[1]))
				addIns("\tadd\t"+register+",\t"+register+",\t1")
				pass	
			elif(line[0] == '--'):
				register = getReg(convName(line[1]))
				addIns("\tsub\t"+register+",\t"+register+",\t1")
				pass
			else:
				pass
	#print "\n----------- MIPS code -----------\n"
	f = open('code.asm', 'wb')
	#print ".data"
	f.write(".data\n")
	for line in data_section:
		#print line
		f.write("%s\n" % line)
	#print ".text"
	f.write(".text\n")
	for line in text_section:
		#print line
		if(line == "main:"):
			f.write("%s\n" % line)
			for line2 in global_text:
				f.write("%s\n" % line2)
		else:
			f.write("%s\n" % line)
	f.close()
	#dump_str = ""
	#f = open('dump.txt', 'wb')
	#f.write("%s" % dump_str)
	#f.close()
	pass


if __name__ == "__main__":
	pass

def calcfn(g1,tk,parentToken,sp):
	#global tokenVal
	#global dump_str
	#if(type(tk) is list):
#		calc_tree(g1,tk[0],parentToken,sp)
#	else:
#		dump_str=dump_str+"\n"+(sp)*"	"+tk.name
#		#print (sp)*"	",tk.name
#		if(not ( mp.has_key(str(tk)) ) ):
#			g1.node(str(tokenVal),str(tk.name))
#			ct = tokenVal
#			tokenVal = tokenVal + 1
#			mp[str(tk)] = ct
#			if(parentToken >= 0):
##				g1.edge(str(parentToken),str(ct))
#			parentToken = ct
#			childNumber = len(tk.astChildList)
#			if childNumber > 0:
#				for j in range(0,childNumber):
#					calc_tree(g1,tk.astChildList[j],parentToken,sp+1)
#		else:
##			ct = mp[str(tk)]
##			if(parentToken >= 0):
#				g1.edge(str(parentToken),str(ct))
	pass
