import os
'''
Things needed for sequence stuff
'''

#read in a fasta supermatrix, returns a hash and a string of the names (csv)
def read_matrix_to_hash(supermatrix, outf):
	
	name = ""
	names = ""
	Hash = {}
	for x in supermatrix:
		x = x.rstrip("\r\n")
		if x[0] == ">":
			if name != "":
				names += name + ","
				Hash[name] = seq
			seq = ""
			name = x[1:]
		else:
			seq += x
	names += name
	if outf:
		outf.write("All taxa: " + names + "\n") 
	Hash[name] = seq
	return Hash,names
	
#Get the gene from the Hash
def length_to_gene_to_folder(gene_name, f_hash, start, stop, out_folder):
	
	start = start - 1
	out = open(out_folder + "/Fasta/" + gene_name, "w")
	for i in f_hash:
		out.write(">" + i + "\n" + f_hash[i][start:stop] + "\n")
		

#Reads in partition file (This codes as elegant as I am)
def read_partition_raxml(part,outf,f_hash,out_folder):
	
	models = ""
	gene_names = ""
	gene_lengths = ""
	for x in part:
		x = x.rstrip("\r\n")
		x = x.replace(" ", "")
		y = x.split(",")
		models += y[0] + ","
		z = y[1].split("=")
		gene_name = z[0] + ".fa"
		gene_names += gene_name + ","
		a = z[1].split("-")
		b = int(a[1]) - int(a[0]) + 1
		gene_lengths += str(b) + ","
		length_to_gene_to_folder(gene_name,f_hash, int(a[0]), int(a[1]), out_folder)
	outf.write("gene names: " + gene_names + "\n")
	outf.write("gene models: " + models + "\n")
	outf.write("gene lengths: " + gene_lengths + "\n")
	return gene_names,models
	
		
		
	
		