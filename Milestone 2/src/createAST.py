import graphviz as gv

mp = {}

tokenVal = 0

def calc_tree(g1,tk,parentToken):
	global tokenVal
	if(not ( mp.has_key(str(tk)) ) ):
		g1.node(str(tokenVal),str(tk.name))
		ct = tokenVal
		tokenVal = tokenVal + 1
		mp[str(tk)] = ct
		if(parentToken >= 0):
			g1.edge(str(parentToken),str(ct))
		parentToken = ct
		childNumber = len(tk.astChildList)
		if childNumber > 0:
			for j in range(0,childNumber):
				calc_tree(g1,tk.astChildList[j],parentToken)
	else:
		ct = mp[str(tk)]
		if(parentToken >= 0):
			g1.edge(str(parentToken),str(ct))
	

	pass


def calc_tree2(g1,tk,parentToken):
	global tokenVal
	#print parentToken
	g1.node(str(tokenVal),str(tk.name))
	if(parentToken >= 0):
		g1.edge(str(parentToken),str(tokenVal))
	tokenVal = tokenVal + 1
	parentToken = tokenVal - 1
	print tk.name,tk
	childNumber = len(tk.astChildList)
	if childNumber > 0:
		for j in range(0,childNumber):
			calc_tree2(g1,tk.astChildList[j],parentToken)

	pass

def create_tree(result,name):
	g1 = gv.Graph(format='svg')
	#g1.node(str(0),str(result.name))
	calc_tree(g1,result,-1)
	filename = g1.render(filename=name+'tree')
	#print filename
	#print(g1.source)
	#print(result)
	#print result.astChildList
	pass


if __name__ == "__main__":
	#result = ('/', ('+', ('NUM', 24), ('NUM', 4)), ('NUM', ))
	create_tree(result)