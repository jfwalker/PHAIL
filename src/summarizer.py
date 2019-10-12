import sys
import os

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


#give it a constraint to start at and it will identify constraints to add in
#while making sure they do not conflict with something in the tree

#Not Working!
def get_tree_from_seed(seed,sorted_likelihoods,bip_hash,con_hash):
	

	hash = {}
	all_hash = {}
	
	#best is taken as a part
	hash[seed[0]] = seed[1]
	
	
	all_hash[seed[0]] = seed[1]
	
	#should be parsing through the list in order of how likely a relationship is
	for i in sorted_likelihoods:
		
		print i[0] + " " + str(i[1])
		#ignore the seed and the no constraint
		if i[0] not in hash and i[0] != "no_constraint":
			
			#check if it has any conflicts with current tree set
			
			#this would mean it has no conflicts so it can't conflict with current tree
			#set
			if len(con_hash[i[0]]) == 0:
				
				hash[i[0]] = i[1]
			
			#This means it does have conflicts so check if those exist in tree set
			else:
				
				#parse the pre-identified conflicts
				for j in con_hash[i[0]]:
					
					if j in hash:
					
						print "conflict is in"
					
					else:
					
						hash[i[0]] = i[1]
				
					
					
	for i in hash:
		print i + "and" + bip_hash[i]
				
				

		

#gets the constraints ordered by their likelihood, need them to be chosen based
#on likelihood and not conflicting with other trees
def find_noncon(sorted_likelihoods,bip_hash,con_hash):

	count = 0
	#get starting seeds (edges with the highest likelihoods), and those that start with
	#an edge that was rejected because it conflicted with something already in the tree
	for i in sorted_likelihoods:
	
		#the array has no constraint still in it so account for that
		if i[0] != "no_constraint":
			if count == 0:
				seed = i
		count += 1	
	get_tree_from_seed(seed,sorted_likelihoods,bip_hash,con_hash)



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










	
	
	