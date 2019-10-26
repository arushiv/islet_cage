import pandas
import numpy as np
import sys
import pybedtools
import scipy.stats
import itertools
import os
import subprocess as sp
import argparse
import time
import pysam

        
def getOpts():
    parser = argparse.ArgumentParser(description="""Subsample bams. Uses samtools flagstat to get total read count """)
    parser.add_argument('--bam', required=True, help="""bam file""")
    parser.add_argument('--coverage', required=True, type=int, help="""Coverage to subsample to """)
    parser.add_argument('--seed', type=int, default=11, help="""seed. Default = 11""")
    parser.add_argument('--output_prefix', required=True,  help="""Output file name prefix. Will output prefix.temp.bam, prefix.bam and prefix.bam.bai """)
    parser.add_argument('--log', required=True,  help="""Log file name.""")

    args = parser.parse_args()

    return args


def get_coverage(bamfile, match_string):
    """Get total reads using samtools flagstat """
    o = pysam.flagstat(bamfile)
    total_reads = int([s for s in o.split('\n') if match_string in s][0].split()[0])
    return total_reads  


if __name__ == '__main__':

    args = getOpts()

    mylog = open(args.log, 'w+')
    sys.stdout = sys.stderr = mylog

    input_index = f"{args.bam}.bai"
    
    if not os.path.isfile(input_index):
        print("Expected bam index does not exist")
        sys.exit(1)
        

    bam_coverage = get_coverage(args.bam, "in total")
    fraction = round(args.coverage/bam_coverage, 2)
    
    print(f"bam coverage was {bam_coverage}, coverage to subsample was {args.coverage}, fraction of coverage_to_subsample/bam_coverage = {fraction}")

    tempfile = f"{args.output_prefix}.temp.bam"
    output_bam = f"{args.output_prefix}.bam"
    output_index = f"{args.output_prefix}.bam.bai"
    
    if fraction >= 1:
        cmd = f'cp {args.bam} {tempfile} ; cp {args.bam} {output_bam}; cp {input_index} {output_index} '
        start = time.time()
        sp.check_output(cmd, shell=True)
        print(f"Ran: {cmd} -- in {time.time() - start} secs")
        
    else:
        value = str(fraction).replace('0.','')
        cmd = f"""samtools view -b -s {args.seed}.{value} {args.bam}  > {tempfile};
        samtools sort {tempfile} -O BAM -@ 8 > {output_bam};
        samtools index {output_bam}
        """
        
        start = time.time()
        sp.check_output(cmd, shell=True)
        subsample_time = time.time()
        print(f"Ran {cmd} -- in { subsample_time - start} secs")
                                                                                                                                                                                                                                            
