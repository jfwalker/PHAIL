import sys
import node
import tree_stuff

def get_left(nd):
	
	left = []
	right = []
	for i in nd.children:

		if i.children and i.label == "":
			left = tree_stuff.tips(left,i)
			return left



def sew_it(ML_val,branches,bip_hash):

	maintree = node.Node()
	names = []
	
	#get the names
	names = tree_stuff.get_tips(bip_hash.itervalues().next())
	lvs = set(names)
	
	
	trees = []
	temp = []
	for i in branches:
		nd = node.Node()
		nd = tree_stuff.build(bip_hash[branches[i]])
		temp = get_left(nd)
		temp = "(" + ",".join(temp) + ");"
		x = tree_stuff.build(temp)
		trees.append(x)
	
	lvsnms = set()
	for i in trees:
		
		for l in i.lvsnms():
			
			lvsnms.add(l)
		
	for i in lvsnms:

		nd = node.Node()
		nd.label = i
		maintree.add_child(nd)
	
	for i in trees:

		mr = tree_stuff.get_mrca_wnms(i.lvsnms(),maintree)
		mvnds = set()
		
		for j in mr.children:
			
			if len(set(j.lvsnms()).intersection(set(i.lvsnms())) ) > 0:
				mvnds.add(j)
		nd = node.Node()
		for j in mvnds:

			mr.remove_child(j)
			nd.add_child(j)
		mr.add_child(nd)
	print maintree.get_newick_repr() + ";"
