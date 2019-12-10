import sys
import os
import tree_stitcher

'''
Series of tools designed to summarise the data
'''

#array
def get_constraint_vals(aa,array,outc):
	
	count = 0
	for i in aa:
		
		line = ""
		line += str(aa[count][0]) + "," + str(aa[count][1])
		for j in array:
		
			line += "," + str(aa[count][j])
		count += 1
		outc.write(line + "\n")


#Take all the data that's been generated and divide it by edge
#I think the complexity of this originates from laziness, probably
#an easy place to gain speed
def divide_out_edges(outd,raxml,cons_confs):

	os.system("mkdir " + outd + "/EdgeAnalyses/")
	
	if raxml == "":
		l_file = open(outd + "/Likelihoods_iqtree.csv")
	else:
		l_file = open(outd + "/Likelihoods_raxml.csv")
	
	#transform the l_file into an array of arrays
	aa = []
	for i in l_file:
		i = i.strip("\r\n")
		a = i.split(",")
		aa.append(a)
	
	for i in cons_confs:
		array = []
		array.append(aa[0].index(i))
		for j in cons_confs[i]:
			array.append(aa[0].index(j))

		outc = open(outd + "/EdgeAnalyses/" + str(i[:-4]) + ".csv", "w")
		get_constraint_vals(aa,array,outc)
		outc.close()
		
#Takes in the likelihood file and returns it in array of arrays format		
def get_aa_of_likefile(likefile):
	
	aa = []
	l_file = open(likefile, "r")
	for i in l_file:
		i = i.strip("\r\n")
		a = i.split(",")
		aa.append(a)
	return aa

#bipartition file to a hash
def bip_to_hash(bip):
	
	bip_hash = {}
	bip_file = open(bip, "r")
	for i in bip_file:
		
		j = i.split(":")
		j[1] = j[1].replace(" ", "((")
		j[1] = j[1].replace("|", "),")
		j[1] = j[1].replace("\n", ");")
		
		bip_hash[j[0]] = j[1]
	bip_file.close()
	
	return bip_hash

#conflict file to a hash
def con_to_hash(con):

	con_hash = {}
	con_file = open(con, "r")
	
	for i in con_file:
		
		i = i.strip("\n\r")
		j = i.split(",")
		con_hash[j[0]] = j[1:]
	return con_hash


def check_seed(seed,sls,con_hash):
	
	#print sls
	stored = set()
	stored_best_tree = {}
	stored.add(seed[0])
	stored_best_tree[seed[1]] = seed[0]
	maybe_future_seeds = []
	future_seeds = []
	
	#parse through in order of likelihood
	for i in sls:

		#ignore the no constraint one
		if i[0] != "no_constraint" and i[0] != seed[0]:
		
			#this means there is an intersection
			if stored.intersection(con_hash[i[0]]):
			
				#print "Cannot Insert: " + str(i[0]) + " value: " + str(i[1])
				string = str(i[0]) + ":" + str(i[1])
				maybe_future_seeds.append(string)
				
			
			#no intersection between the conflict and what's going in
			else:
				#print "inserted: " + i[0] + " value: " + str(i[1])
				stored.add(i[0])
				stored_best_tree[i[1]] = i[0]
				if len(maybe_future_seeds) != 0:
					future_seeds.extend(maybe_future_seeds)
					maybe_future_seeds = []
				
				
	#print "The highest edge tree has: " + str(len(future_seeds)) + " edges with values higher than those placed"
	
	#for i,j in sorted(stored_best_tree.items(), key=lambda p:p[1]):
		#print "Seed " + seed[0] + " biparts: " + str(i) + " " + str(j)
	
	return stored_best_tree,future_seeds
				
			
			

		

#gets the constraints ordered by their likelihood, need them to be chosen based
#on likelihood and not conflicting with other trees
def find_noncon(sorted_likelihoods,bip_hash,con_hash,test):

	count = 0
	#get starting seeds (edges with the highest likelihoods), and those that start with
	#an edge that was rejected because it conflicted with something already in the tree
	for i in sorted_likelihoods:
	
		#the array has no constraint still in it so account for that
		if i[0] != "no_constraint":
			if count == 0:
				seed = i
			count += 1
		else:
			#get the top likelihood value
			best_val = i[1]

	stored_best_tree,future_seeds = check_seed(seed,sorted_likelihoods,con_hash)
	
	#gives a tree with the likelihood painted on it
	if test == "tree" or test == "trees":
		tree_stitcher.sew_it(best_val,stored_best_tree,bip_hash)
	
	#gives the difference between the best and the constraint
	if test == "tree_dist" or test == "constraint_label" or test == "blank":
		tree_stitcher.sew_it2(best_val,stored_best_tree,bip_hash,test)

	for i in future_seeds:
		
		#
		other_trees,ignored = check_seed(i.split(":"),sorted_likelihoods,con_hash)
		
		if test == "tree" or test == "trees":
			tree_stitcher.sew_it(best_val,other_trees,bip_hash)
		
		if test == "tree_dist" or test == "constraint_label" or test == "blank":
			tree_stitcher.sew_it2(best_val,other_trees,bip_hash,test)
		#print other_trees
	
	#get_tree_from_seed(seed,sorted_likelihoods,bip_hash,con_hash)



#take in an array where 0 is constraints and 1 is likelihoods and sort them by
#highest value
def sort_largest(summed_likelihoods):

	a = []
	sort = []
	
	#sort an array
	a = summed_likelihoods[1]
	results = map(float, a)
	sort = sorted(results, reverse=True)

	ordered = []
	#find the new index
	for i in sort:
		
		a = []
		a.append(summed_likelihoods[0][results.index(i)])
		a.append(summed_likelihoods[1][results.index(i)])
		ordered.append(a)
		
	return ordered

#take in an array where 0 is constraints and 1 is likelihoods and sort them by
#highest value
def sort_largest_force(forces,summed_likelihoods):

	ordered = []
	hash = {}
	front_array = []
	ordered = sort_largest(summed_likelihoods)
	for x in forces:
		hash[x] = x
	for x in ordered:
		if x[0] in hash:
			ordered.remove(x)
			ordered[:0] = [x]
	return ordered
			


#this will sum the likelihood and return a matrix, where 0 is the constraints
#and 1 is the summed likelihoods
def col_like_test(aa,s):

	a = []
	likesum = []
	likesum.append(aa[0][1:])
	for i in aa[1:]:
		
		count = 0
		for j in i[1:]:
			
			if len(a) == 0:
				a = [0.0] * len(i[1:])
			a[count] += float(j)
			count += 1
	likesum.append(a)
	return likesum










	
	
	