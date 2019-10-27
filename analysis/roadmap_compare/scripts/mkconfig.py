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

cmd = f"wget --directory-prefix={BASE_DIR}/data/roadmap_chromatin_states; tar -xvzf {BASE_DIR}/data/roadmap_chromatin_states/all.mnemonics.bedFiles.tgz"

sp.check_output(cmd, shell=True)
config.update({
    'DATA':{
        'features' : get_path("work/annotations/{feature}.bed"),
        'hg19_lengths' : get_path("data/hg19_lengths.txt"),
        'roadmap_cells' : get_path("data/roadmap_chromatin_states/roadmap_cells.tsv"),
        'roadmap_bed_files': get_path("data/roadmap_chromatin_states/{cell}_18_core_K27ac_mnemonics.bed.gz"),
        'roadmap_color' : get_path("data/roadmap_chromatin_states/colormap_18_core_K27ac.tab"),
        'roadmap_state' : get_path("data/roadmap_chromatin_states/browserlabelmap_18_core_K27ac.tab"),
        'gencode_pc' : get_path("data/tsslist_gencodev19_pc.bed")
    },
    'SCRIPTS':{
        'plot_roadmap_cluster' : get_path("analysis/roadmap_compare/scripts/chromhmm_roadmap_cluster.R"),
        'plot_roadmap_cluster_simple' : get_path("analysis/roadmap_compare/scripts/plot.roadmap_compare_clean.R")
    },
    'FEATURES' : ["Islets.tcs", "Islets.tc_in_all_enhancer", 'Islets.tc_in_all_promoter','Islets.tc_in_peak_in_all_enhancer','Islets.tc_in_peak_in_all_promoter'],
    'SELECT' : ['Islets.tc_in_peak_in_all_enhancer', 'Islets.tc_in_peak_in_all_promoter']
})

with open(config_file, 'w+') as f:
    yaml.dump(config, f, default_flow_style=False)

        




