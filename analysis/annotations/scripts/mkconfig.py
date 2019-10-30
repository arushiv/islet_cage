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
    'chromatin_states': get_path("data/chromhmm/selected_annotated_states/files_by_state/cell4_11.Islets.{state}.bed"),
    'atac_peaks': get_path("data/atac_seq/final_peaks/Islets.broadPeaks_fdr0.01_noBlacklist.bed"),
    'tcs': get_path("data/call_tcs/tissue_tcs_formatted/tc_paraclu.Islets.tpmThresh2singletonThresh2.minExpIn10.noblacklist.bed"),
    'tcs_with_strand': get_path("data/call_tcs/tissue_tcs/tc_paraclu.Islets.tpmThresh2singletonThresh2.minExpIn10.noblacklist.bed"),
    'hg19': get_path("data/hg19_chromsizes.bed")
})

                      
with open(config_file, 'w+') as f:
    yaml.dump(config, f, default_flow_style=False)



