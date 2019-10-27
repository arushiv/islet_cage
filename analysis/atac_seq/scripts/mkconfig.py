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
    'sample_info': get_path("analysis/atac_seq/configs/sample_info.tsv"),
    'map_env': get_path("env/map.yaml"),
    'peak_env': get_path("env/peaks.yaml"),

    # Types of MACS2 peaks called:
    'peak_type' :["broad","narrow"],

    # For final selected peaks, two samples within a tissue were merged after subsampling
    # Each sample of a tissue was subsampled to a different depth to keep the final peak territory
    # roughly similar. These selected subsample thresholds were:
    'select_peaks': {
        'Islets': 18000000,
    },

    # IF only certain libraries have to be run, specify here.
    # If this is empty sting (""), all libraries in file sample info will be run
    'libraries': "",

    # Library type. if "single_end" specified, consider read1 only for all libraries and use cutadapt.
    # Default leave this as an empty string ""
    'uniform_end' : "single_end",  # ""
    'cutadapt': {
        # TSV to specify adapter type and sequence
        'adapters' : get_path("data/atac_seq/adapters.tsv")
    },

    # Trim reads to length. leave empty string if this is not needed
    'trim_reads_to': " --length 36 ",
    
    # subsample bam files? A number of subsamplings were tried:
    'subsample_type': [14000000, 15000000, 18000000, 20000000, 24000000, 30000000],
    'scripts': {
        'subsample_bam' : get_path("analysis/atac_seq/scripts/subsample_bams.py")
    },
    'bwa_index':{
        'hg19': os.getenv("bwa_index"),
    },
    'whitelist':{},
    'blacklist':{
        'hg19': [ get_path("data/wgEncodeDukeMapabilityRegionsExcludable.bed.gz"),
                  get_path("/wgEncodeDacMapabilityConsensusExcludable.bed.gz")]
    }
})

                      
with open(config_file, 'w+') as f:
    yaml.dump(config, f, default_flow_style=False)

        


# In[10]:




