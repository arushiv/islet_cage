#!/usr/bin/env python
import yaml
import sys
import os
import subprocess as sp
import argparse

def getOpts():
    parser = argparse.ArgumentParser(description='Make config files for CAGE workflows')
    parser.add_argument('--base', required=True, help="""base directory""")
    parser.add_argument('--email', required=True, help="""email""")
    parser.add_argument('--config', required=True, help="""config file path""")
    parser.add_argument('--workflow', required=True, help="""workflow name to make configs for""")
    args = parser.parse_args()
    return args

args = getOpts()
BASE_DIR = args.base
email = args.email
config_file = args.config
workflow = args.workflow

def get_path(dirname):
    return os.path.join(BASE_DIR, dirname)

ANALYSIS_DIR = get_path(f'analysis/{workflow}')
results = get_path(f'work/{workflow}')
CONFIG_DIR = os.path.join(ANALYSIS_DIR, 'configs')

config = {'email': email,
          'results': results}

config.update({
    'chromsizes': get_path("data/hg19.chrom_sizes"),
    # chromatin_states
    'histone_chromatin_states': get_path("work/chromhmm/selected_annotated_states/cell4_11.{tissue}.dense.bed"),
    'tcs': get_path("work/call_tcs/tcs/tissue_tcs/tc_paraclu.{tissue}.tpmThresh2singletonThresh2.minExpIn10.noblacklist.bed"),
    'atac_peaks': get_path("work/atac_seq/final_peaks/{tissue}.broadPeaks_fdr0.01_noBlacklist.bed"),
    'fantom_tcs': get_path("data/fantom_tcs.bed"),
    #FANTOM individual TCs
    'fantom_tissue_tcs': get_path("work/compare_with_fantom/tcs/tc_paraclu.{fantom_tissue}.tpmThresh2singletonThresh2.bed"),
    'fantom_tissues': '[t for t in glob_wildcards(config["fantom_tissue_tcs"])[0] if "Universal" not in t ]',
    'atac_bedgraph': get_path("work/atac_seq/macs2/subsamp_{subsample}_merged/{tissue}_treat_pileup.bdg"),
    'atac_bam': get_path("work/atac_seq/subsampled_bam/{tissue}.subsamp_{subsample}_merged.bam"),
    'subsamplings':{
        'Islets': 18000000
    },
    'tissues': ["Islets"]
})
                      
with open(config_file, 'w+') as f:
    yaml.dump(config, f, default_flow_style=False)

        




