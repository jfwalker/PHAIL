# PHAIL
PHylogenetic Analysis Into Lineages

Under development

EdgeTest.py has been moved to the repo [EdgeTest](https://github.com/jfwalker/EdgeTest/)

## Important Note about iqtree2
If you are using iqtree2 PHAIL is now reporting the likelihood for the fast likelihood tree search using GTR+I+G mode, I'll be editing it shortly to report the likelihood from the full search



Basic info: This is a program to evaluate all edges and then consolidate them into a tree. This also provides a variety of summary statistics that let you investigate how similar one edge is to another.

As of right now the program will only work on complete datasets (e.g complete gene occupancy for all taxa)

Importantly this program is possible thanks to some really great other programs so if you use either of these please cite their respective software!

[raxml-ng](https://github.com/amkozlov/raxml-ng)

[iqtree](http://www.iqtree.org/)

### Options

The program has the following options

```-c``` This is the checkpoint, if a run has died for some reason then give the logfile as the input here and it will start where it left off. No other commands are required in this case.

```-q``` This is required and is the partition/model file in raxml format.

```-s``` This is also required and is the supermatrix that corresponds to the model file.

```-t``` This is required and is a set of trees that you plan to investigate (e.g break into their edges and analyze the likelihood of the edges)

```-d``` This is the number of threads (default is 2)

```-r``` This is for raxml-ng, if you use this cite the raxml-ng [paper!!!](https://github.com/amkozlov/raxml-ng)

```-i``` This is for iqtree, again if you use this cite the iqtree [paper!!!](http://www.iqtree.org/)

```-l``` This is the name for the log file, by default it is creatively named log.log

```-f``` This is the name you want for the output folder, by default it will write to a folder called output_folder

```-v``` This is the support value, it will ignore any edges below this value

```-z``` This is the more verbose output, but it's actually not much more verbose and designed to write over itself so I would recommend running it 

### Example

A simple example with the test dataset would be

```EX: python src/PHAIL.py -s test_data/Test.fa -q test_data/test.model -t test_data/Test.tre -r raxml-ng```

Then assuming you accidently kill it so you can change it to verbose mode, restart from where it leaves off with

```EX: python2.7 src/PHAIL.py -c log.log -z```

### Output folder

In this folder you will find a number of things

```Constraints/``` These are all the unique edges that were found and then analyzed

```EdgeAnalyses/``` This is the likelihoods for the edges divided out by the edge and then listed with all edges that conflict with that edge

```Fasta/``` This is the supermatrix separated into fastas

```Likelihoods_raxml.csv``` or ```Likelihoods_iqtree.csv``` depending on what you ran. This will have all edges and all likelihoods for those edges.

```bipartitions.txt``` This is all the edges that were found and what constraint they are associated with

```conflicts.txt``` This is whichever edges conflict with eachother

```iqtree_outputs``` or ```raxml_outputs``` This is all the output files from the respective programs run

### Once PHAIL.py is finished

At this point, assuming the program finished without programs, the data can be dissected and analyzed.

To do this you'll want to run the program ```tree_assembler.py```

To assemble the Tree(s) run the program as follows:

```EX: python src/tree_assembler.py -l output_folder/Likelihoods_raxml.csv -b output_folder/bipartitions.txt -c output_folder/conflicts.txt -m tree```

And the program will print out the trees that were made in the tree building procedure and one tree where any conflicting edges among the previous tree(s) are collapsed.

The options for ```tree_assembler.py``` are as follows

```-l``` This is the likelihood file produced from PHAIL.py

```-b``` This is the bipartition file produced

```-c``` This is the file with the conflicts

```-m``` This is the method of analysis. If you are going to evaluate how the edges (These will be in the EdgeAnalysis folder) you can use the edge or edge_con options. The option edge will print the likelihoods of all constraints. The option edge_con will compare how many genes will support a given edge based on a users specified support value. This can be specified with ```-s```. For tree building it follows the procedure in figure 1 of the paper, the main difference in the options is what support value you give. Assuming, you go with tree it will simply put the likelihood of the edge as the support value. Assuming you go with blank it will not put anything on the edge. The option tree_dist will give you the difference between having a constraint and not having a constraint. The option constraint label will give you the constraint file each edge corresponds to. The option 2_con will give you the difference between the edge in the tree and the best score for an edge that conflicts with it. The option 2_con_gene is the 2_con value divided by the number of genes. The option con_b is the number of conflicting edges with the edge in the tree. The option conflict will put on the total number of genes that have a superior value for the edge over any other edge, it also requires you to provide a support value with ```-s```. The support value of 0.0 will give all genes conflicting with the edge in the tree, a value of 2.0 will give all that conflict and have a log-likelihood of 2 or more etc.

```-f``` This will force a constraint to exist, or more than one as long as they are given in a comma separated list. For example since constraint_7.tre in the tree is not more likely than the one that gets placed (constraint_11.tre) but conflicts with constraint_7.tre, then it will make sure the first tree has constraint_7.tre in it and then proceed to the rest of the tree building procedure from figure 1 in the paper.

```EX: python src/tree_assembler.py -l output_folder/Likelihoods_raxml.csv -b output_folder/bipartitions.txt -c output_folder/conflicts.txt -m constraint_label -f constraint_7.tre```

Running it with a forced suboptimal constraint will provide a set of trees and an edge consensus tree (the last one output) that has a collapsed edge. This can also occur when edges conflict with one another during the tree assembly procedure.

If you have any questions feel free to reach out to me at my email jfwalker at umich.edu. Hope this helps!









