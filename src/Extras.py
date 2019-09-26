from datetime import datetime
import sys
import os

'''
Set of extra stuff, not essential for functions
'''


#Basic time thingy
def get_time(position, outfile):
	now = datetime.now()
	dt_string = now.strftime("%B %d, %Y %H:%M:%S")
	if outfile:
		print position + " " + dt_string
		outfile.write(position + " " + dt_string + "\n")
	else:
		print position + " " + dt_string

#For restarting runs
def get_checkpoint_info(logfile):
	
	finished_genes = []
	for x in logfile:
		x = x.strip("\n\r")
		if x[0:12] == "Folder named":
			y = x.split(" ")
			folder_name = y[2]
		if x[0:11] == "gene names:":
			all_genes = x[12:][:-1].split(",")
		if x[0:12] == "gene models:":
			gene_models = x[13:][:-1].split(",")
		if x[0:13] == "Finished gene":
			y = x.split(" ")
			z = all_genes.index(y[2])
			all_genes.pop(z)
			gene_models.pop(z)
		if x[0:15] == "you are running":
			y = x.split(" ")
			program = y[3]
			path = y[5]
	
	return ",".join(all_genes), ",".join(gene_models), folder_name, program, path

	