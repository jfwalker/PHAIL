import sys
import argparse
import os
import subprocess
import Extras
import seq_stuff
import tree_stuff
import likelihood_estimation_stuff
import summarizer

'''
PHylogenetic Analysis Into Lineages
'''
def generate_argparser():

	parser = argparse.ArgumentParser(
        prog="PHAIL.py",
        )
	parser.add_argument("-s", "--supermatrix", required=False, type=str, help="""
	Supermatrix file in fasta, if not fasts use pxs2fa from the phyx package""")
	parser.add_argument("-q", "--partition", required=False, type=str, help="""
	Partition file, should be in RAxML readable format""")
	parser.add_argument("-t", "--trees", required=False, type=str, help="""
	List of trees to analyze for conflicts""")
	parser.add_argument("-d", "--Threads", required=False, type=str, help="""
	default is 2""")
	parser.add_argument("-r", "--raxml", required=False, type=str, help="""
	Location and name of raxml, defaul is raxml""")
	parser.add_argument("-i", "--iqtree", required=False, type=str, help="""
	Location and name of iqtree, defaul in path""")
	parser.add_argument("-l", "--log", required=False, type=str, help="""
	Log file name, default is log.log""")
	parser.add_argument("-f", "--folder", required=False, type=str, help="""
	Name of the folder""")
	parser.add_argument("-c", "--checkpoint", required=False, type=str, help="""
	Give the logfile and let the program take over from where it left off""")
	parser.add_argument("-v", "--support_value", required=False, type=str, help="""
	Only take into account relationships with this value or better, if a clade does
	not have a support value it is automatically evaluated""")
	parser.add_argument("-z", "--verbosity", action="count", default=0, help="""
	Reports when a likelihood has been calculated for each constraint (recommended if you screen watch)""")
	return parser
	
	
def main(arguments=None):
	

	parser = generate_argparser()
	args = parser.parse_args(arguments)
	Extras.get_time("Run Starting", None)
	
	if args.checkpoint == None and args.partition == None:
		print "Killed run, need either a checkpoint or files to run. For a simple reverse concatenate run without trees. For info type PHAIL.py -h"
		Extras.get_time("Run killed", None)
		sys.exit()
	
	if args.checkpoint:
		print "Reading in " + args.checkpoint
		logfile = args.checkpoint
		checkfile = open(logfile, "r")
		#Read in and get all the stuff from the checkpoint log file
		gene_names,gene_models,output_folder,program,path = Extras.get_checkpoint_info(checkfile)
		gene_names += ","
		gene_models += ","
		raxml = ""
		iqtree = ""
		if program == "iqtree":
			outl = open(output_folder + "/Likelihoods_iqtree.csv", "a")
			l_file = open(output_folder + "/Likelihoods_iqtree.csv", "r")
			constraint_list = l_file.readline()[:-1].split(",")[2:]
			iqtree = path
		else:
			outl = open(output_folder + "/Likelihoods_raxml.csv", "a")
			l_file = open(output_folder + "/Likelihoods_raxml.csv", "r")
			constraint_list = l_file.readline()[:-1].split(",")[2:]
			raxml = path
		
		checkfile.close()
		
		#re-initiate the logfile
		outf = open(logfile, "a")
		Extras.get_time("Run Re-starting", outf)

		
	if args.log and args.checkpoint == None:
		outf = open(args.logfile)	
		#Use start as a way of ensuring the logfile is what it is
		outf.write("-----Log File-----\n")
		Extras.get_time("Log file made", None)
		Extras.get_time("Settings: " + str(args), outf)
			
	elif args.log == None and args.checkpoint == None:
		outf = open("log.log","a")
		outf.write("-----Log File-----\n")
		Extras.get_time("Log file made", None)
		Extras.get_time("Settings: " + str(args), outf)
		
	if args.folder and args.checkpoint == None:
		output_folder = args.folder
		os.system("mkdir " + output_folder)
		message = "Folder named " + output_folder
		Extras.get_time(message, outf)
	
	elif args.folder == None and args.checkpoint == None:
		output_folder = "output_folder"
		os.system("mkdir output_folder")
		message = "Folder named " + output_folder
		Extras.get_time(message, outf)
		
		
	if args.supermatrix and args.checkpoint == None:
		sup = open(args.supermatrix,"r")
		SupermatrixHash,names = seq_stuff.read_matrix_to_hash(sup,outf)
		message = "Supermatrix read in and named " + args.supermatrix
		Extras.get_time(message, outf)
	
	elif args.supermatrix == None and args.checkpoint == None:
		print "Needs either a supermatrix or a checkpoint file :("
		print "Did not exit in case you want to reverse concatenate"
		Extras.get_time("No supermatrix", outf)
		
	
	if args.partition and args.checkpoint == None:
		part = open(args.partition,"r")
		os.system("mkdir " + output_folder + "/Fasta/")
		Extras.get_time("Fasta Folder Made", outf)
		gene_names,gene_models = seq_stuff.read_partition_raxml(part,outf,SupermatrixHash,output_folder)
		Extras.get_time("Partition File read in and fastas divided by genes", outf)
	
	elif args.partition == None and args.checkpoint == None:
		print "Needs either a partition or a checkpoint file :("
		Extras.get_time("Died", outf)	
		sys.exit()
	
	if args.trees and args.checkpoint == None:
		tr = open(args.trees,"r")
		os.system("mkdir " + output_folder + "/Constraints/")
		Extras.get_time("Constraint Folder Made", outf)
		biparts = []
		if args.support_value:
			biparts = tree_stuff.dissect_trees(tr, names, int(args.support_value))
		else:
			biparts = tree_stuff.dissect_trees(tr, names, 0)
		constraint_list = tree_stuff.make_constraints(biparts, output_folder, outf)
		message = "Found " + str(len(biparts)) + " unique biparts, constraints in folder"
		Extras.get_time(message, outf)
			
	elif args.trees == None and args.checkpoint == None:
		print "Needs set of newick trees :("
		Extras.get_time("Died", outf)	
		sys.exit()
	
	'''	
	Variables needed for downstream
	array of constraints (constraint_list), 
	gene fasta names (gene_names), 
	models (gene_models)
	'''
	
	if args.raxml and args.iqtree:
		print "You specified both raxml and iqtree"
		sys.exit()
	elif args.raxml:
		iqtree = ""
		raxml = args.raxml
		message = "you are running raxml from " + raxml
		Extras.get_time(message, outf)	
	elif args.iqtree:
		raxml = ""
		iqtree = args.iqtree
		message = "you are running iqtree from " + iqtree
		Extras.get_time(message, outf)
	elif args.iqtree == None and args.raxml == None and args.checkpoint == None:
		iqtree = "iqtree"
		raxml = ""
		message = "you are running iqtree from " + iqtree
		Extras.get_time(message, outf)
	
	if args.Threads:
		threads = args.Threads
	else:
		threads = "2"
	
	#likelihood file
	if args.checkpoint:
		print "Checking Likelihood file"
	elif args.iqtree:
		outl = open(output_folder + "/Likelihoods_iqtree.csv", "a")
		outl.write("gene_name,no_constraint," + ",".join(constraint_list) + "\n")
	elif args.raxml:
		outl = open(output_folder + "/Likelihoods_raxml.csv", "a")
		outl.write("gene_name,no_constraint," + ",".join(constraint_list) + "\n")
	elif args.iqtree == None and args.raxml == None and args.checkpoint == None:
		outl = open(output_folder + "/Likelihoods_iqtree.csv", "a")
		outl.write("gene_name,no_constraint," + ",".join(constraint_list) + "\n")
		
	

	#Easy to add in parallel processing to this part
	if raxml == "" and gene_names != ",":
		likelihood_estimation_stuff.calc_likelihood_iqtree(constraint_list, gene_names, gene_models, iqtree, threads, output_folder, outf, outl, args.verbosity)
	elif raxml != "" and gene_names != ",":
		likelihood_estimation_stuff.rax_runner(constraint_list, gene_names, gene_models, raxml, threads, output_folder, outf, outl, args.verbosity)

	message = "Finished running edges, getting conflicts among biparts"
	Extras.get_time(message, outf)
	cons_confs = tree_stuff.get_conflicts(output_folder)
	
	
	message = "Summarizing constraints by conflict, see " + output_folder + " for details"
	Extras.get_time(message, outf)
	#I think it's l file that should be added here
	summarizer.divide_out_edges(outl,output_folder)
	
	
if __name__ == "__main__":
	main()