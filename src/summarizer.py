import sys
import os

'''
Series of tools designed to summarise the data
'''

#Take all the data that's been generated and divide it by edge
def divide_out_edges(outl,outd):

	os.system("mkdir " + outd + "/EdgeAnalyses/")
	print "Here"