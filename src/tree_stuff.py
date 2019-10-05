'''
Tree procedures and stuff
'''
import sys
from node import Node
import Extras

#This takes in the newick and the
#seq data then puts them in a data
#structure that can be preorder or
#postorder traversed pretty easily
def build(instr):
	#print "Entered build"
	root = None
	name_array =[]
	index = 0
	nextchar = instr[index]
	begining = "Yep"
	keepgoing = True
	current_node = None
	#keeps going until the value becomes false
	while keepgoing == True:
		#This situation will only happen at the very beginning but
		#when it hits this it will create a root and change begining
		#to no
		if nextchar == "(" and begining == "Yep":
				
			root = Node()
			current_node = root
			begining = "No"
		#This happens anytime their is an open bracket thats not the
		#beginning
		elif nextchar == "(" and begining == "No":
		
			newnode = Node()
			current_node.add_child(newnode)
			current_node = newnode
		#This indicates that you are in a clade and tells the 
		#program to move back one to grab the sister to the clade
		elif nextchar == ',':
		
			current_node = current_node.parent
		#This says you are closing a clade and therefore it moves
		#back to where the parent node is which allows the name
		#to be added to the parent node
		elif nextchar == ")":
			#print "Closing Clade"
			current_node = current_node.parent
			index += 1
			nextchar = instr[index]
			while True:
			
				if nextchar == ',' or nextchar == ')' or nextchar == ':' \
					or nextchar == ';' or nextchar == '[':
					break
				name += nextchar
				index += 1
				nextchar = instr[index]
			current_node.label = name
			index -= 1
		#This indicates everything is done so keepgoing becomes false
		elif nextchar == ';':
		
			keepgoing = False
			break
		#This indicates you have branch lengths so it grabs the branch
		#lengths turns them into floats and puts them in the current node
		elif nextchar == ":":
			index += 1
			nextchar = instr[index]
			while True:
				if nextchar == ',' or nextchar == ')' or nextchar == ':' \
					or nextchar == ';' or nextchar == '[':
					break
				branch += nextchar
				index += 1
				nextchar = instr[index]
			current_node.length = float(branch)
			index -= 1
		#This is for if anywhitespace exists
		elif nextchar == ' ':
		
			index += 1
			nextchar = instr[index]
		#This is for when any taxa name is hit, it will concatenate
		#the taxa names together and add the name
		else: # this is an external named node
		
			newnode = Node()
			current_node.add_child(newnode)
			current_node = newnode
			current_node.istip = True
			while True:
				if nextchar == ',' or nextchar == ')' or nextchar == ':' \
					or nextchar == ';' or nextchar == '[':
					break
				name += nextchar
				index += 1
				nextchar = instr[index]
			current_node.label = name
			name_array.append(name)
			index -= 1
		if index < len(instr) - 1:
			index += 1
		nextchar = instr[index]
		name = ""
		branch = ""
	return root


#get segments of a bipart
def clade_post_order(clade,clade_names):
	
	for x in clade.children:
		if x.istip:
			clade_names.append(x.label)
		clade_post_order(x,clade_names)
	return clade_names

#Post order traverse the whole tree
def post_order(tree,support,all_names,t_to_clade):
	
	for x in tree.children:
		#account for trees that don't have support
		if x.children and x.label == "":
			#print "Clade does not have support value"
			clade_names = []
			clade = []
			clade_names = clade_post_order(x,clade_names)
			clade = get_right(clade_names, all_names)
			t_to_clade.append(clade)
			
		elif x.children and support <= int(x.label):
			#print "Clade has support value: " + x.label
			clade_names = []
			clade = []
			clade_names = clade_post_order(x,clade_names)
			clade = get_right(clade_names, all_names)
			t_to_clade.append(clade)
			
		post_order(x,support,all_names,t_to_clade)
	return t_to_clade

#get the other side of the bipartition
def get_right(clade_names, all_names):

	mis1 = list(set(all_names.split(",")) - set(clade_names))
	clade_names.append("|")
	return ",".join(clade_names + mis1)

def comp_biparts(tree_bipart,all_biparts):
	
	bi = tree_bipart.split("|")
	part1 = bi[0][:-1].split(",")
	part2 = bi[1][1:].split(",")
	
	for x in all_biparts:
		comp_bi = x.split("|")
		comp_part1 = comp_bi[0][:-1].split(",")
	
		if len(part1) == len(comp_part1):
			dif = list(set(part1) - set(comp_part1))
			if len(dif) == 0:
				return True
		if len(part2) == len(comp_part1):
			dif = list(set(part2) - set(comp_part1))
			if len(dif) == 0:
				return True
	return False
	
#compare if any incoming biparts are new
#can add in bipart counts
def get_biparts(trees_clades, all_biparts):
	
	new_biparts = []
	count = 0
	for x in trees_clades:
		bin = comp_biparts(x,all_biparts)
		if bin == False:
			new_biparts.append(x)
	return new_biparts

#ugh...this is ugly
def dissect_trees(tr,all_names,support):
	
	all_biparts = []
	count = 0
	for x in tr:
		
		sys.stderr.write("tree " + str(count) + "\r")
		t_to_clade = []
		new_biparts = []
		
		x = x.rstrip("\r\n")
		tree = build(x)

		trees_clades = post_order(tree,support,all_names,t_to_clade)
		
		if len(all_biparts) == 0:
			all_biparts = trees_clades
		else:
			new_biparts = get_biparts(trees_clades, all_biparts)
			all_biparts += new_biparts
		
		count += 1
	return all_biparts
			
def make_constraints(biparts, out_folder, outf):
	
	outb = open(out_folder + "/bipartitions.txt", "w")
	count = 0
	constraint_list = []
	for x in biparts:
		
		constraint_name = "constraint_" + str(count) + ".tre"
		c = x.split("|")
		out = open(out_folder + "/Constraints/" + constraint_name, "w")
		
		#checks for 2 to account for the split leading to a blank one
		if len(c[0].split(",")) == 2 or len(c[1].split(",")) == 2:
			message = "can't make constraint for \"" + x + "\" it may be rooted"
			Extras.get_time(message, outf)
		
		constraint = "((" + c[0][:-1] + ")" + c[1] + ");"
		outb.write(constraint_name + ": " + c[0][:-1] + "|" + c[1][1:] + "\n")
		out.write(constraint)
		
		constraint_list.append(constraint_name)
		count += 1
	return constraint_list


#check to see if two bipartitions conflict with one another
def conflict_check(bipart1,bipart2):
	
	bi = bipart1.split("|")
	bipart1_part1 = bi[0].split(",")
	bipart1_part2 = bi[1][0:].split(",")
	bi2 = bipart2.split("|")
	bipart2_part1 = bi2[0].split(",")
	bipart2_part2 = bi2[1][0:].split(",")
	
	#print str(bipart1_part2) + " comp " + str(bipart2_part2)
	
def get_conflicts(outd):

	bips = open(outd + "/bipartitions.txt", "r")

	#parse existing bipartitions
	b = []
	for i in bips:
		a = i.split(": ")
		a[1] = a[1].rstrip("\n\r")
		b.append(a)
	
	#run all against all
	for i in b:

		for j in b:
		
			conflict_check(i[1],j[1])
		
			




	
		
	
