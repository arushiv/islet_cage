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
    'barcode_counts' : get_path("data/starr_seq/final_counts_table.txt"),
    'subassembly' : get_path("data/starr_seq/VRE_{config}_strm_enhancer.haps.final.txt"),
    'pools': ["TCs"],
    'configs': ["SCP1_promoter_dwn"],
    'minDNA': [1, 5, 10, 20],
    'minBarcodes': [1, 2, 4],
    'SCRIPTS': {
        'organize_data': get_path("analysis/starr-seq/scripts/organize_starrseq_barcode_insert_counts.py"),
        'format': get_path("analysis/starr-seq/scripts/format_results_for_mpra.py"),
        'mpra_analyze': get_path("analysis/starr-seq/scripts/mpra_analyze.R")
    }
})


with open(config_file, 'w+') as f:
    yaml.dump(config, f, default_flow_style=False)

        




