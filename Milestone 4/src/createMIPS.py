data_section = []
text_section = []
vtr = {}
rtv = {}

def create_mips(code):
	global data_section
	global text_section
	print "----------- MIPS -----------\n"
	for line in code:
		print line
		if(line != []):
			if(line[0] == 'BEGINFUCTION'):
				text_section += [line[2]+':']
				pass
			elif(line[0] == 'ENDFUNCTION'):
				text_section += ["\tli	$v0, 10"]
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
				data_section += ['\tVAR_'+line[2]+'\t.space\t'+str(data_size)]
				pass
			elif(line[0] == 'LABEL'):
				text_section += [line[1]+':']
				pass
			elif(line[0] == 'GOTO'):
				pass
			elif(line[0] == '+'):
				pass
			elif(line[0] == '-'):
				pass
			elif(line[0] == '='):
				pass
			else:
				pass
	print "\n----------- MIPS code -----------\n"
	print ".data"
	for line in data_section:
		print line
	print ".text"
	for line in text_section:
		print line
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
