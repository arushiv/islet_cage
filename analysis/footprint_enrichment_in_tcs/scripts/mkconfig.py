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
    'DATA': {
        'segment': get_path("data/footprints/Islet-intersect.{segment}.Footprints.bed"),
        'annotation': get_path("work/annotations/{annotation}.bed"),
        'workspace': get_path("data/islet-intersect-peaks/Islet-intersect.broadPeaks.bed.gz"),
        'output': "{segment}.annot_{annotation}.gatResults.dat",
        'count_output': "", #"E{state}.chromstate_{annotation}.%s.countsOutput"
        'log': "{segment}.annot_{annotation}.gatLog.dat",
        'fig_output': "enrichment_GAT.pdf"
    },
    'PARAMETERS':{
        'SEGMENTS': "glob_wildcards(config['DATA']['segment'])[0]",
        'ANNOTATIONS': "['Islets.tc_in_peak_in_all_enhancer', 'Islets.tc_in_peak_in_all_promoter', \
        'Islets.tc_flanking_downstream_500', 'Islets.tc_flanking_upstream_500']",
        'num_samples': 10000,
        'filenameString': "*.gatResults.dat",
        'colnames': "footprint extra tissue annotation", # leave as "" if not using
        'split_delimiter': "."  # leave as "" if not using
    },
    'SCRIPTS': {
        'compileResults': get_path("analysis/footprint_enrichment_in_tcs/scripts/analyze_GATResults.py"),
        'plot': get_path("analysis/tc_enrichment_in_annotations/scripts/plot.py")
    }
})

with open(config_file, 'w+') as f:
    yaml.dump(config, f, default_flow_style=False)

        




