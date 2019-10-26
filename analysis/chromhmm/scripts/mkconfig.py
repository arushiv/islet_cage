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

# Use ChromHMM to run models with various number of states. Select model that best captures information
# Use Chromhmm overlap enrichment with previously published states in matching cell types to annotate new states
# To start with bed files converted from bam
# H3K4me1 used for PNAS paper was low quality, use one sample from Pasquali et al 2014. This ChIP-seq dataset does
# not have a WCE control, control column corresponding to this should be left blank in the
# chromhmm marks table

config.update({
    'PARAMETERS' :{
        'chosen_k4me1_library': "ERS353630",  # This was chosen based on phantompeakqualtools
        'selected_model': 11, # 11 state model was chosen as it captured relevant states and compared well with other N state models
        'cell_nos': ["cell4"],  # Histone data for four cell types will be taken
        'cell_types': { # list the cell types
            'cell4' : ["Islets", "SkeletalMuscle", "Adipose", "Liver"]
        },
        'marks': ['WCE', 'H3K4me3', 'H3K4me1', 'H3K27ac', 'H3K27me3', 'H3K36me3'],   # List the ChIP-seq marks
        'control' : "WCE",
        'custom_wce' : {
            'cell': "Islets",
            'mark': "H3K4me1",
            'wce': "",
        },
        'assembly' : "hg19_concise",
        
        # Number of states to run ChromHMM with
        'minStates': 8,
        'numStates' : 16,
        
        # subsample bed files to mean coverage within a mark
        'subsample' : {
            'H3K27ac': 28123470,
            'H3K27me3': 53603910,
            'H3K36me3': 63763910,
            'H3K4me1': 63441280,
            'H3K4me3': 62220940,
            'WCE': 109214300},
    }
})

with open(config_file, 'w+') as f:
    yaml.dump(config, f, default_flow_style=False)

        




