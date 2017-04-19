data_section = []
text_section = []

addressDescriptor = {}
registerDescriptor = { '$t0' : None, '$t1' : None, '$t2' : None, '$t3' : None, '$t4' : None, '$t5' : None,  '$t6' : None, '$t7' : None, '$t8' : None, '$t9' : None, '$s0' : None, '$s1' : None, '$s2' : None, '$s3' : None, '$s4' : None }
freeRegisters = ['$s4','$s3','$s2','$s1','$s0','$t9', '$t8', '$t7', '$t6', '$t5', '$t4',  '$t3', '$t2', '$t1', '$t0']
busyRegisters = []

declaredVars = []

def isVar(var):
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
				text_section += ["\tlw\t"+register+",\t"+var]
	return register


def create_mips(code):
	global data_section
	global text_section
	global declaredVars
	print "----------- Three Address Code -----------\n"
	for line in code:
		print line
		if(line != []):
			if(line[0] == 'BEGINFUCTION'):
				text_section += [line[2]+':']
				pass
			elif(line[0] == 'ENDFUNCTION'):
				text_section += ["\tli\t$v0,\t10"]
				text_section += ["\tsyscall"]
				#jr    $ra
				pass
			elif(line[0] == 'VARDECLARATION'):
				data_size = 0
				if(line[1]=='void'): 
					data_size=0
				elif(line[1]=='char'): 
					data_size=1
				elif(line[1]=='bool'): 
					data_size=1
				elif(line[1]=='short'):
					data_size=2
				elif(line[1]=='int'): 
					data_size=4
					data_section += ['\tVAR_'+line[2]+':\t.word\t0']
					declaredVars.append('VAR_'+line[2])
				elif(line[1]=='long'): 
					data_size=8
				elif(line[1]=='float'): 
					data_size=4
				elif(line[1]=='double'): 
					data_size=8
				elif(line[1]=='signed'): 
					data_size=4
				elif(line[1]=='unsigned'): 
					data_size=4
				else:
					pass
				#data_section += ['\tVAR_'+line[2]+'\t.space\t'+str(data_size)]
				pass
			elif(line[0] == 'LABEL'):
				text_section += [line[1]+':']
				pass
			elif(line[0] == 'GOTO'):
				text_section += ["\tb\t"+line[1]]
				pass
			elif(line[0] == 'IF'):
				if(line[2] == "=="):
					register = line[1]
					register3 = line[3]
					if(isVar(line[1])):
						register = getReg('VAR_'+line[1])
					if(isVar(line[3])):
						register3 = getReg('VAR_'+line[3])
					text_section += ["\tbeq\t"+register+",\t"+register3+",\t"+line[5]]
				elif (line[2] == "<"):
					register = line[1]
					register3 = line[3]
					if(isVar(line[1])):
						register = getReg('VAR_'+line[1])
					if(isVar(line[3])):
						register3 = getReg('VAR_'+line[3])
					text_section += ["\tblt\t"+register+",\t"+register3+",\t"+line[5]]
				elif (line[2] == ">"):
					register = line[1]
					register3 = line[3]
					if(isVar(line[1])):
						register = getReg('VAR_'+line[1])
					if(isVar(line[3])):
						register3 = getReg('VAR_'+line[3])
					text_section += ["\tbgt\t"+register+",\t"+register3+",\t"+line[5]]
				elif (line[2] == "<="):
					register = line[1]
					register3 = line[3]
					if(isVar(line[1])):
						register = getReg('VAR_'+line[1])
					if(isVar(line[3])):
						register3 = getReg('VAR_'+line[3])
					text_section += ["\tble\t"+register+",\t"+register3+",\t"+line[5]]
				elif (line[2] == ">="):
					register = line[1]
					register3 = line[3]
					if(isVar(line[1])):
						register = getReg('VAR_'+line[1])
					if(isVar(line[3])):
						register3 = getReg('VAR_'+line[3])
					text_section += ["\tbge\t"+register+",\t"+register3+",\t"+line[5]]
				else:
					pass
				pass
			elif(line[0] == 'PRINTINT'):
				text_section += ["\tli\t$v0,\t1"]
				if(isVar(line[1])):
					register = getReg('VAR_'+line[1])
					text_section += ["\tmove\t$a0,\t"+register]
				else:
					text_section += ["\tli\t$a0,\t"+line[1]]
				text_section += ["\tsyscall"]
				pass
			elif(line[0] == '+'):
				register = getReg('VAR_'+line[1])
				register2 = line[2]
				register3 = line[3]
				if(isVar(line[2])):
					register2 = getReg('VAR_'+line[2])
				if(isVar(line[3])):
					register3 = getReg('VAR_'+line[3])
				text_section += ["\tadd\t"+register+",\t"+register2+",\t"+register3]
				pass
			elif(line[0] == '-'):
				register = getReg('VAR_'+line[1])
				register2 = line[2]
				register3 = line[3]
				if(isVar(line[2])):
					register2 = getReg('VAR_'+line[2])
				if(isVar(line[3])):
					register3 = getReg('VAR_'+line[3])
				text_section += ["\tsub\t"+register+",\t"+register2+",\t"+register3]
				pass
			elif(line[0] == '*'):
				register = getReg('VAR_'+line[1])
				register2 = line[2]
				register3 = line[3]
				if(isVar(line[2])):
					register2 = getReg('VAR_'+line[2])
				if(isVar(line[3])):
					register3 = getReg('VAR_'+line[3])
				text_section += ["\tmul\t"+register+",\t"+register2+",\t"+register3]
				pass
			elif(line[0] == '/'):
				register = getReg('VAR_'+line[1])
				register2 = line[2]
				register3 = line[3]
				if(isVar(line[2])):
					register2 = getReg('VAR_'+line[2])
				if(isVar(line[3])):
					register3 = getReg('VAR_'+line[3])
				text_section += ["\tdiv\t"+register+",\t"+register2+",\t"+register3]
				pass
			elif(line[0] == '='):
				register = getReg('VAR_'+line[1])
				if(isVar(line[2])):
					register2 = getReg('VAR_'+line[2])
					text_section += ["\tmove\t"+register+",\t"+register2]
				else:
					text_section += ["\tli\t"+register+",\t"+line[2]]
				pass
			elif(line[0] == '++'):
				register = getReg('VAR_'+line[1])
				text_section += ["\tadd\t"+register+",\t"+register+",\t1"]
				pass
			elif(line[0] == '--'):
				register = getReg('VAR_'+line[1])
				text_section += ["\tsub\t"+register+",\t"+register+",\t1"]
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
