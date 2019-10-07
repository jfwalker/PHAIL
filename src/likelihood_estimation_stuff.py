import os
import subprocess
import Extras
import sys

'''
Different tools to calculate the likelihood using iqtree or raxml
'''
#~/Desktop/iqtree-1.6.12-MacOSX/bin/iqtree -g output_folder/Constraints/constraint_0.tre -s EmpiricalExample/Test.fa -pre output_folder/constraint_0_Test.fa

#calculate likelihood without the constraint
def no_const_iqtree(iqtree, threads, output_folder, gene_name, model):
	
	if model == "DNA" or model == "AA":
		cmd = iqtree + " -redo -nt " + threads + " -s " + output_folder + "/Fasta/" + gene_name + " -pre " + output_folder + "/iqtree_outputs/" + gene_name
	else:
		cmd = iqtree + " -redo -nt " + threads + " -s " + output_folder + "/Fasta/" + gene_name + " -m " + str(model) + " -pre " + output_folder + "/iqtree_outputs/" + gene_name
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
	t = p.communicate()[0].split("\n")
	for i in t:
		if i[0:23] == "Optimal log-likelihood:":
			return str(i[24:])

#calculate likelihood without the constraint
def const_iqtree(iqtree, threads, output_folder, gene_name, model, constraint):	
	
	if model == "DNA" or model == "AA":
		cmd = iqtree + " -redo -nt " + threads + " -s " + output_folder + "/Fasta/" + gene_name + " -g " + output_folder + "/Constraints/" + constraint  + " -pre " + output_folder + "/iqtree_outputs/" + gene_name + "_" + constraint
	else:
		cmd = iqtree + " -redo -nt " + threads + " -m " + str(model) + " -s " + output_folder + "/Fasta/" + gene_name + " -g " + output_folder + "/Constraints/" + constraint  + " -pre " + output_folder + "/iqtree_outputs/" + gene_name + "_" + constraint
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
	t = p.communicate()[0].split("\n")
	for i in t:
		if i[0:23] == "Optimal log-likelihood:":
			return str(i[24:])
def no_const_raxml(raxml, threads, output_folder, gene_name, model):
	
	if model == "DNA":
		cmd = raxml + " --redo --msa " + output_folder + "/Fasta/" + gene_name + " --threads " + threads + " --model GTR+G --force" + " --prefix " + output_folder + "/raxml_outputs/" + gene_name
	elif model == "AA":
		cmd = raxml + " --redo --msa " + output_folder + "/Fasta/" + gene_name + " --threads " + threads + " --model LG+G --force" + " --prefix " + output_folder + "/raxml_outputs/" + gene_name
	else:
		cmd = raxml + " --redo --msa " + output_folder + "/Fasta/" + gene_name + " --threads " + threads + " --model " + model + " --force" + " --prefix " + output_folder + "/raxml_outputs/" + gene_name
	#print cmd
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
	t = p.communicate()[0].split("\n")
	for i in t:
		if i[0:20] == "Final LogLikelihood:":
			return str(i[21:])
			
def const_raxml(raxml, threads, output_folder, gene_name, model,constraint):
	
	if model == "DNA":
		cmd = raxml + " --redo --msa " + output_folder + "/Fasta/" + gene_name + " --threads " + threads + " --model GTR+G --force --tree-constraint " + output_folder + "/Constraints/" + constraint + " --prefix " + output_folder + "/raxml_outputs/" + gene_name + "_" + constraint
	elif model == "AA":
		cmd = raxml + " --redo --msa " + output_folder + "/Fasta/" + gene_name + " --threads " + threads + " --model LG+G --force --tree-constraint " + output_folder + "/Constraints/" + constraint + " --prefix " + output_folder + "/raxml_outputs/" + gene_name + "_" + constraint
	else:
		cmd = raxml + " --redo --msa " + output_folder + "/Fasta/" + gene_name + " --threads " + threads + " --model " + model + " --force --tree-constraint " + output_folder + "/Constraints/" + constraint + " --prefix " + output_folder + "/raxml_outputs/" + gene_name + "_" + constraint
	#print cmd
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
	t = p.communicate()[0].split("\n")
	for i in t:
		if i[0:20] == "Final LogLikelihood:":
			return str(i[21:])
				
#main iqtree likelihood calc section	
def calc_likelihood_iqtree(constraint_list, gene_names, gene_models, iqtree, threads, output_folder, outf, outl, verbosity):
	
	
	verbose_folder = output_folder + "/iqtree_outputs/"
	os.system("mkdir " + verbose_folder)
	count = 0
	for x in gene_names[:-1].split(","):
		
		likelihoods = ""
		best_likelihood = no_const_iqtree(iqtree, threads, output_folder, x, gene_models[:-1].split(",")[count])
		if best_likelihood == None:
			print "No likelihood calculated, has this been run? Maybe run from log file with -c"
			sys.exit()
		likelihoods += x + "," + best_likelihood
		const_count = 1
		for y in constraint_list:
			best_likelihood = const_iqtree(iqtree, threads, output_folder, x, gene_models[:-1].split(",")[count],y)
			if best_likelihood == None:
				print "No likelihood calculated, has this been run? Maybe run from log file with -c"
				sys.exit()
			likelihoods += "," + best_likelihood
			if verbosity == 1:
				sys.stderr.write("This is gene " + str(count) + " of " + str(len(gene_names[:-1].split(",")) - 1) + " with constraint # " + str(const_count) + " of " + str(len(constraint_list)) + " likelihood is " + str(best_likelihood) + "\r")
			const_count += 1
		outl.write(likelihoods + "\n")
		count += 1
		message = "Finished gene: " + x
		Extras.get_time(message, outf)
			
def rax_runner(constraint_list, gene_names, gene_models, raxml, threads, output_folder, outf, outl, verbosity):

	verbose_folder = output_folder + "/raxml_outputs/"
	os.system("mkdir " + verbose_folder)
	count = 0
	
	for x in gene_names[:-1].split(","):
		likelihoods = ""
		best_likelihood = no_const_raxml(raxml, threads, output_folder, x, gene_models[:-1].split(",")[count])
		if best_likelihood == None:
			print "No likelihood calculated, this typically occurs when a likelihoods has already been calculated during a previous run? Maybe run from log file with -c"
			sys.exit()
		likelihoods += x + "," + best_likelihood
		const_count = 1
		for y in constraint_list:
			best_likelihood = const_raxml(raxml, threads, output_folder, x, gene_models[:-1].split(",")[count],y)
			if best_likelihood == None:
				print "No likelihood calculated, has this been run? Maybe run from log file with -c"
				sys.exit()
			likelihoods += "," + best_likelihood
			if verbosity == 1:
				sys.stderr.write("This is gene " + str(count) + " of " + str(len(gene_names[:-1].split(",")) - 1) + " with constraint # " + str(const_count) + " of " + str(len(constraint_list)) + " likelihood is " + str(best_likelihood) + "\r")
			const_count += 1
		outl.write(likelihoods + "\n")
		count += 1
		message = "Finished gene: " + x
		Extras.get_time(message, outf)

