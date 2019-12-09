import sys
import node
import tree_stuff

def get_left(nd,lvs):
	
	left = []
	right = []
	for i in nd.children:

		if i.children and i.label == "":
			left = tree_stuff.tips(left,i)
			right = list(lvs - set(left))

			return left,right



def sew_it(ML_val,branches,bip_hash):

	maintree = node.Node()
	names = []
	
	#get the names
	names = tree_stuff.get_tips(bip_hash.itervalues().next())
	lvs = set(names)
	
	
	trees = []
	trees_r = []
	temp = []
	temp_r = []
	for i in branches:
		nd = node.Node()
		nd = tree_stuff.build(bip_hash[branches[i]])
		temp,temp_r = get_left(nd,lvs)
		temp = "(" + ",".join(temp) + ");"
		temp_r = "(" + ",".join(temp_r) + ");"
		x = tree_stuff.build(temp)
		trees.append(x)
		x = tree_stuff.build(temp_r)
		trees_r.append(x)
	
	#print trees
	#print trees_r
	lvsnms = set()
	for i in trees:
		
		for l in i.lvsnms():
			
			lvsnms.add(l)
	for i in trees_r:
		
		for l in i.lvsnms():
			
			lvsnms.add(l)

	for i in lvsnms:

		nd = node.Node()
		nd.label = i
		maintree.add_child(nd)
	
	for i in range(0,len(trees)):

		ilvs = trees[i].lvsnms()
		mr1 = tree_stuff.get_mrca_wnms(trees[i].lvsnms(),maintree)
		mr2 = tree_stuff.get_mrca_wnms(trees_r[i].lvsnms(),maintree)
		if mr1 == maintree and mr2 != maintree:
			mr = mr2
			ilvs = trees_r[i].lvsnms()
		else:
			mr = mr1		
		mvnds = set()
		
		for j in mr.children:
			
			if len(set(j.lvsnms()).intersection(set(ilvs)) ) > 0:
				mvnds.add(j)
		nd = node.Node()
		for j in mvnds:

			mr.remove_child(j)
			nd.add_child(j)
		mr.add_child(nd)

	print maintree.get_newick_repr(False) + ";"
