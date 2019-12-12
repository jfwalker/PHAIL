import sys
import node
import tree_stuff
'''
Ugh...So much laziness, I need to rewrite this
'''



def get_left(nd,lvs):
	
	left = []
	right = []
	for i in nd.children:

		if i.children and i.label == "":
			left = tree_stuff.tips(left,i)
			right = list(lvs - set(left))

			return left,right


#Lazy repeat of below
def sew_it2(ML_val,branches,bip_hash,test):

	maintree = node.Node()
	names = []

	#get the names
	names = tree_stuff.get_tips(bip_hash.itervalues().next())
	lvs = set(names)
	
	
	trees = []
	trees_r = []
	temp = []
	temp_r = []
	
	#put trees into an array
	for i in branches:
		
		if test == "2_con":
			nd = node.Node()
			nd = tree_stuff.build(bip_hash[i])
			temp,temp_r = get_left(nd,lvs)
		else:
			nd = node.Node()
			nd = tree_stuff.build(bip_hash[branches[i]])
			temp,temp_r = get_left(nd,lvs)
		
		if test == "tree_dist":
			diffval = ML_val - float(i)
		elif test == "constraint_label":
			diffval = branches[i]
		elif test == "2_con":
			diffval = branches[i]
		elif test == "blank":
			diffval = ""
		temp = "(" + ",".join(temp) + ")" + str(diffval) + ";"
		temp_r = "(" + ",".join(temp_r) + ")" + str(diffval) + ";"
		x = tree_stuff.build(temp)
		trees.append(x)
		x = tree_stuff.build(temp_r)
		trees_r.append(x)

	#print trees
	#print trees_r
	
	#get the tip names as an tree structures
	lvsnms = set()
	for i in trees:
		#print i
		for l in i.lvsnms():
			
			lvsnms.add(l)
	for i in trees_r:
		
		for l in i.lvsnms():
			
			lvsnms.add(l)
	
	#Create a star tree with all tips being tree structures
	for i in lvsnms:

		nd = node.Node()
		nd.label = i
		maintree.add_child(nd)
	
	for i in range(0,len(trees)):

		ilvs = trees[i].lvsnms()
		bp1 = tree_stuff.get_mrca_wnms(trees[i].lvsnms(),maintree)
		bp2 = tree_stuff.get_mrca_wnms(trees_r[i].lvsnms(),maintree)
		
		if bp1 == maintree and bp2 != maintree:
			bp = bp2
			ilvs = trees_r[i].lvsnms()
			#bp.label = trees_r[i].label
		else:
			bp = bp1		
			#bp.label = trees[i].label
		mvnds = set()
		for j in bp.children:

			if len(set(j.lvsnms()).intersection(set(ilvs)) ) > 0:
				mvnds.add(j)
		
		nd = node.Node()
		
		lab = trees_r[i].label
		for j in mvnds:
			#print "Here is j:" + str(j)
			bp.remove_child(j)
			nd.add_child(j)
		if nd.label == "":
			nd.label = lab
		bp.add_child(nd)


	print maintree.get_newick_repr(False) + ";"

#this made my brain hurt so much
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
	
	#put trees into an array
	for i in branches:
		nd = node.Node()
		nd = tree_stuff.build(bip_hash[branches[i]])
		temp,temp_r = get_left(nd,lvs)
		temp = "(" + ",".join(temp) + ")" + str(i) + ";"
		temp_r = "(" + ",".join(temp_r) + ")" + str(i) + ";"
		x = tree_stuff.build(temp)
		trees.append(x)
		x = tree_stuff.build(temp_r)
		trees_r.append(x)

	#print trees
	#print trees_r
	
	#get the tip names as an tree structures
	lvsnms = set()
	for i in trees:
		#print i
		for l in i.lvsnms():
			
			lvsnms.add(l)
	for i in trees_r:
		
		for l in i.lvsnms():
			
			lvsnms.add(l)
	
	#Create a star tree with all tips being tree structures
	for i in lvsnms:

		nd = node.Node()
		nd.label = i
		maintree.add_child(nd)
	
	for i in range(0,len(trees)):

		ilvs = trees[i].lvsnms()
		bp1 = tree_stuff.get_mrca_wnms(trees[i].lvsnms(),maintree)
		bp2 = tree_stuff.get_mrca_wnms(trees_r[i].lvsnms(),maintree)
		
		if bp1 == maintree and bp2 != maintree:
			bp = bp2
			ilvs = trees_r[i].lvsnms()
			#bp.label = trees_r[i].label
		else:
			bp = bp1		
			#bp.label = trees[i].label
		mvnds = set()
		for j in bp.children:

			if len(set(j.lvsnms()).intersection(set(ilvs)) ) > 0:
				mvnds.add(j)
		
		nd = node.Node()
		
		lab = trees_r[i].label
		for j in mvnds:
			#print "Here is j:" + str(j)
			bp.remove_child(j)
			nd.add_child(j)
		if nd.label == "":
			nd.label = lab
		bp.add_child(nd)


	print maintree.get_newick_repr(False) + ";"
