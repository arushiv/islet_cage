
# coding: utf-8
import pandas
import numpy
import math
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
import glob
import time
from scipy import stats
import pybedtools
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams.update({'font.size': 12})
import matplotlib.backends.backend_pdf
from scipy.stats import pearsonr
from matplotlib.backends.backend_pdf import PdfPages
import argparse


# Info from Jacob:
# These are named based upon which basal promoter is used (SCP1 or INS1) and whether the cloned fragment is upstream of the promoter or downstream of the 3' UTR. The columns within each file identify the barcode (readgroupid), the identity of the tile sequence (refname), and any variants detected (synthesis or sequencing errors, with multiple reads used to rule out the latter - column variant_list which is a comma-sep'd list of refname:pos:ref:alt entires).  Perhaps for an initial analysis you might either ignore these variants or only consider perfectly matching entries (in which case that column would read "apparently_wt_no_passing_vars" or "no_variants_input")
# 
# Some barcodes may be common between different configurations, remove these
# Filter for minimum DNA counts of barcodes

def getOpts():
    parser = argparse.ArgumentParser(description="""Organize starr seq barcode count data and subsassembly data""")
    parser.add_argument('--barcode_counts', required=True, help="""Barcode counts file """)
    parser.add_argument('--subassembly', required=True, help="""Subassembly files for each config""")
    parser.add_argument('--barcode_to_remove', help="""List of barcodes to remove""")
    parser.add_argument('--config', required=True, type=str, help="""Name of the config""")
    parser.add_argument('--pool', nargs='+', required=True, type=str, help="""Name of the pool""")
    parser.add_argument('--minDNA', type=int, default=1,  help="""DNA count filters""")
    parser.add_argument('--minBarcode', type=int, default=1,  help="""Min number of qualifying barcodes per insert""")
    parser.add_argument('--output', required=True,  help="""Output file name""")
    parser.add_argument('--log', required=True,  help="""Log file name.""")
    args = parser.parse_args()

    return args


if __name__ == '__main__':

    args = getOpts()

    log = open(args.log, 'w+') 
    sys.stdErr = sys.stdOut = log
    # Read counts data, filter out barcodes with all 0 RNA counts
    counts = pandas.read_csv(args.barcode_counts,
                             header=None, sep='\t',
                             names=['barcode', 'rep1', 'rep2', 'rep3', 'dna'])

    counts['barcode'] = counts['barcode'].map(lambda x: x.strip())
    
    # Remove barcodes with all 0 RNA counts
    counts = counts[~ (counts['rep1'] + counts['rep2'] + counts['rep3'] == 0)]

    # Read subassembly file
    subassembly = pandas.read_csv(args.subassembly, sep='\t',
                                  usecols=['readgroupid', 'passes', 'refname', 'status', 'n_variants_passing']) 

    # Remove barcodes common between configurations -
    if args.barcode_to_remove is not None:
        with open(args.barcode_to_remove) as f:
            exclude_barcodes = f.readlines()

        exclude_barcodes = [x.rstrip() for x in exclude_barcodes]
        subassembly = subassembly[~ subassembly['readgroupid'].isin(exclude_barcodes)]

    # Merge barcode counts with subassembly barcodes
    cdf = pandas.merge(counts, subassembly, how='inner', left_on="barcode", right_on="readgroupid")
    cdf['config'] = args.config
    cdf['pool'] = cdf['refname'].map(lambda x: x.split('_')[0])

    # Select relevant pool
    cdf = cdf[cdf['pool'].isin(args.pool)]
    
    # Filter for  min DNA count threshold 
    cdf = cdf[cdf['dna'] >= args.minDNA]
    cdf['minDNA'] = args.minDNA
    
    # Get qualifying barcode counts per insert
    insert_count = pandas.DataFrame(cdf.groupby('refname').size()).reset_index()
    qualifying_inserts = insert_count[insert_count[0] >= args.minBarcode]['refname'].tolist()

    cdf = cdf[cdf['refname'].isin(qualifying_inserts)]
    cdf['minBarcode'] = args.minBarcode

    cdf.to_csv(args.output, sep='\t', index=False, na_rep="NA")
    log.close()
