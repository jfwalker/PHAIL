open(nexus,$ARGV[0])||die "perl ConvertNexToPart.pl NexusFile.nex";
while($line = <nexus>){

	chomp $line;
	if ($line =~ /  charset /){

		$name = ($line =~ m/  charset (.*?);/)[0];
		push @array, $name;

	}elsif($line =~ /:/){
	
		$len = ($line =~ m/    (.*?):.*/)[0];
		push @array2, $len;
	
	}
}
foreach $i (0..$#array){

	print "$array2[$i], $array[$i]\n";

}