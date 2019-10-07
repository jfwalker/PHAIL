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
	method of summarizing data you want to use (edge,tree)""")
	parser.add_argument("-s", "--support", required=False, type=str, help="""
	support metric or in edge analysis cutoff""")
	return parser
	
def main(arguments=None):
	
	parser = generate_argparser()
	args = parser.parse_args(arguments)
	
	if args.like_file:
		aa = summarizer.get_aa_of_likefile(args.like_file)
	
	if args.bipartition:
		bip_hash = summarizer.bip_to_hash(args.bipartition)
		
	if args.method:
		test = args.method
	
	
	if test == "edge":
		print test
		
	
	



if __name__ == "__main__":
	main()