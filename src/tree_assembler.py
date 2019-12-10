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
	method of summarizing data you want to use [\"edge\"",\"tree\",\"tree_dist\",\"constraint_label\"]""")
	parser.add_argument("-s", "--support", required=False, type=str, help="""
	support metric or in edge analysis cutoff""")
	return parser
	
def main(arguments=None):
	
	parser = generate_argparser()
	args = parser.parse_args(arguments)
	
	#turns the likelihood file into an array of arrays
	if args.like_file:
		aa = summarizer.get_aa_of_likefile(args.like_file)
	
	#turns the bipartitions file into a hash, where one has the bipartition, and the
	#values are the edge constraints
	if args.bipartition:
		bip_hash = summarizer.bip_to_hash(args.bipartition)
	
	if args.conflicts:
		con_hash = summarizer.con_to_hash(args.conflicts)
	
	if args.method:
		test = args.method
		
		#generate the consensus trees underlying the data
		if test == "trees" or test == "tree":
			summed_likelihoods = summarizer.col_like_test(aa,args.support)
			sorted_likelihoods = summarizer.sort_largest(summed_likelihoods)
			non_conflicting_sort = summarizer.find_noncon(sorted_likelihoods,bip_hash,con_hash,test)
			
		if test == "tree_dist" or test == "constraint_label" or test == "blank":
			summed_likelihoods = summarizer.col_like_test(aa,args.support)
			sorted_likelihoods = summarizer.sort_largest(summed_likelihoods)
			non_conflicting_sort = summarizer.find_noncon(sorted_likelihoods,bip_hash,con_hash,test)
		
		
		if test == "edge":
			summed_likelihoods = summarizer.col_like_test(aa,args.support)
			sorted_likelihoods = summarizer.sort_largest(summed_likelihoods)
			for x in sorted_likelihoods:
				print x
			
		
	
	



if __name__ == "__main__":
	main()