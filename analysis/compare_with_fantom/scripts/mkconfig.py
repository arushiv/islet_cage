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

cmd = f"wget --directory-prefix={BASE_DIR}/data/fantom -r --no-parent -A '*.ctss.bed.gz' http://fantom.gsc.riken.jp/5/datafiles/latest/basic/human.tissue.hCAGE/ ; \
wget http://fantom.gsc.riken.jp/5/datafiles/latest/basic/human.tissue.hCAGE/00_human.tissue.hCAGE.hg19.assay_sdrf.txt --directory-prefix={BASE_DIR}/data/fantom"
sp.check_output(cmd, shell=True)

config.update({
    'DATA':{
        'raw': "data/fantom/*.ctss.bed.gz",
        'srdf': "data/fantom/00_human.tissue.hCAGE.hg19.assay_sdrf.txt",
        'pancreas_ctss': "data/fantom/pancreas%2c%20adult%2c%20donor1.CNhs11756.10049-101G4.hg19.ctss.bed.gz"
    },
    'SCRIPTS':{
        'tc_cage':get_path( "analysis/call_tcs/scripts/tc_cage.R")
    }
})

with open(config_file, 'w+') as f:
    yaml.dump(config, f, default_flow_style=False)

        




