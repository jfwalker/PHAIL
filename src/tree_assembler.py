import sys
import argparse
import os
import summarizer


'''
Tree Assembler, different ways of condensing PHAIL output
'''
def generate_argparser():

	parser = argparse.ArgumentParser(
        prog="tree_assembler.py",
        )
	parser.add_argument("-l", "--like_file", required=True, type=str, help="""
	likelihood file or an edge file from PHAIL""")
	parser.add_argument("-b", "--bipartition", required=False, type=str, help="""
	bipartition file from PHAIL""")
	parser.add_argument("-c", "--conflicts", required=False, type=str, help="""
	constraint conflicts file from PHAIL""")
	parser.add_argument("-m", "--method", required=False, type=str, help="""
	method of summarizing data you want to use [\"edge\"",\"tree\",\"tree_dist\",\"constraint_label\",\"blank\",\"2_con\",\"2_con_gene",\"con_b\",\"conflict\"]""")
	parser.add_argument("-s", "--support", required=False, type=str, help="""
	support cutoff [to be implemented]""")
	parser.add_argument("-f", "--force_edge", required=False, type=str, help="""
	comma separated list of edges to be in final tree""")
	return parser
	
def main(arguments=None):
	
	parser = generate_argparser()
	args = parser.parse_args(arguments)
	
	#turns the likelihood file into an array of arrays
	if args.like_file:
		aa = summarizer.get_aa_of_likefile(args.like_file)
		genes = len(aa) - 1
	
	#turns the bipartitions file into a hash, where one has the bipartition, and the
	#values are the edge constraints
	if args.bipartition:
		bip_hash = summarizer.bip_to_hash(args.bipartition)
	
	if args.conflicts:
		con_hash = summarizer.con_to_hash(args.conflicts)
	
	if args.method:
		
		gene_count_hash = {}
		test = args.method
		
		#generate the consensus trees underlying the data
		if test == "trees" or test == "tree" or test == "tree_dist" or test == "constraint_label" or test == "blank" \
		or test == "2_con" or test == "2_con_gene" or test == "con_b" or test == "conflict":
			summed_likelihoods = summarizer.col_like_test(aa,args.support)
		
			if test == "conflict":
				if args.support:
				
					gene_count_hash = summarizer.get_gene_sums_all(aa,con_hash,args.support)
				
				else:
					print "'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''"
					print "You've specified conflict but no support, I would recommend 2.0 but I      "
					print "don't want to impose anything. So go with what you think is best. Keep     "
					print "in mind this is not the same as number of genes conflicting on an ML tree. "
					print "This is number of genes where the constraint is at X cutoff better.        "
					print "'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''"
					sys.exit()
			#sorts likelihoods but forces specified ones to the top
			if args.force_edge:
				array = args.force_edge.split(",")
				sorted_likelihoods = summarizer.sort_largest_force(array,summed_likelihoods,con_hash)
			else:
				sorted_likelihoods = summarizer.sort_largest(summed_likelihoods)
			non_conflicting_sort = summarizer.find_noncon(genes,sorted_likelihoods,bip_hash,con_hash,test,gene_count_hash)
		
		
		if test == "edge":
			summed_likelihoods = summarizer.col_like_test(aa,args.support)
			sorted_likelihoods = summarizer.sort_largest(summed_likelihoods)
			
			for x in sorted_likelihoods:
				if x[0] != "no_constraint":
					print str(x) + " " + bip_hash[x[0]]
				else:
					print str(x)



if __name__ == "__main__":
	main()