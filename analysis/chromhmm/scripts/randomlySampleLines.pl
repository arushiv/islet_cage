#!/usr/bin/perl -w

use strict;
use Getopt::Long qw(GetOptions);
use Data::Dumper;

# Steve Parker
# stephen.parker@nih.gov
# 23 July 2010


# get command line options:
my ( $h, $fraction, $total );



GetOptions(
	   'h'   => \$h,
	   'f=f' => \$fraction,
	   't=i' => \$total,
	   );

my $usage = <<USAGE;
USAGE: perl randomlySampleLines.pl -f <fraction_to_sample>

    options:
    -h display this help message
    -f fraction of line to randomly sample from STDIN (floating point number)
    -t total number of lines to sample (integer, only works as an upper limit, not a lower limit)



    EXAMPLE:
    cat someFile.txt | perl randomlySampleLines.pl -f 0.01 > someFileRandom0.01.txt

    # the above command will randomly sample approximately 1% of the lines from the file piped from STDIN




USAGE

# check command line arguments and display help if needed
unless ($fraction) { die "$usage"; }
if     ($h)        { die "$usage"; }













my $count = 0;



while ( my $line = <> ) {


    if (rand() < $fraction) {
	print "$line";
	$count++;
    }
    
    if ($total) {
	if ($count == $total) {
	    last;
	}
    }

}


exit();
