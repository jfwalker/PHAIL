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

def edge_test(aa,s):

	if s == None:
		s = 2.0
	print s
	
	
	