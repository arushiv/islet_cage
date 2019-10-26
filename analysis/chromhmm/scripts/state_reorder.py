
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
import argparse
plt.switch_backend('agg')
import json


def gp(mdir, prefix, name):
    return os.path.join(mdir, f"{prefix}.{name}")

def rot(g):
    for i, ax in enumerate(g.fig.axes):   ## getting all axes of the fig object
        ax.set_xticklabels(ax.get_xticklabels(), rotation = 90)

def save(name):
    plt.savefig(name, bbox_inches="tight")
    

def getOpts():
    parser = argparse.ArgumentParser(description="""Annotate chromatin states""")
    parser.add_argument('--color', required=True, help="""color codes for PNAS states """)
    parser.add_argument('--model', required=True, help="""ChromHMM model file""")
    parser.add_argument('--overlap_enrich', required=True, help="""File output from ChromHMM overlap enrich with genome % and state enrichment values """)
    parser.add_argument('--overlap_enrich_cell', required=True, help="""Cell type for which overlap enrich is being used """)
    parser.add_argument('--segment_dir', required=True, help="""Directory with ChromHMM segments. All *segments.bed wull be globbed""")
    parser.add_argument('--reorder_dir', required=True,  help="""Directory for all output. Output files will all have prefix supplied""")
    parser.add_argument('--reorder_files_dir', required=True,  help="""Output directory for reordered files by state.""")
    parser.add_argument('--prefix',   help="""Output file prefix.""")
    parser.add_argument('--custom_states', type=json.loads,  help="""Custom names for certain states.""")
    args = parser.parse_args()

    return args
                                
def make_track_bed(segment, gen, outputfile):
    
    d = pandas.read_csv(segment, sep='\t', header=None, 
                        names=['chrom', 'start', 'end', 'state'])
    d = pandas.merge(d, gen[['state','name','color']], how="inner", on="state")
    d['score'] = 0
    d['strand'] = "."
    d['blockCount'] = 1
    d['blockStarts'] = 0
    d['blockSizes'] = d['end'] - d['start']
    d['thickStart'] = d['start']
    d['thickEnd'] = d['end']
    d = d[['chrom','start','end','name','score','strand','thickStart','thickEnd','color','blockCount','blockSizes','blockStarts']]
    d.sort_values(['chrom','start','end'], inplace=True)
    d.to_csv(outputfile, sep='\t', index=False, header=False)
    return d[['chrom','start','end','name']]


def get_files_by_state(d, cell, outputdir):
    for name, group in d.groupby('name'):
        outfilename = gp(outputdir, prefix, f"{cell}.{name}.bed")
        group.to_csv(outfilename, sep='\t', index=False, header=False)

        
def makeHeatmap(model, outputfile, order):
    dm = pandas.read_csv(model, header=None, names=['result','state','marknum','mark','yes-no','prob'], sep="\t")
    dm = dm[(dm['result']=="emissionprobs") & (dm['yes-no']==1.0)][['state','mark','prob']]
    newdm = dm.pivot(index='state',columns='mark', values='prob')
    newdm = newdm[['H3K4me3','H3K27ac','H3K4me1','H3K36me3','H3K27me3']]
    print(newdm)
    
    if order is not None:
        newdm.index = pandas.CategoricalIndex(newdm.index, categories = order)
        newdm.sort_index(level=0, inplace=True)

    newdm.reset_index(inplace=True)
    newdm.index = newdm.index + 1
    newdm.drop('state', axis=1, inplace=True)

    plt.figure(figsize=(6, 9))
    g = sns.heatmap(newdm, cmap="Blues", linecolor="black", linewidths=0.3,
               cbar_kws = {'use_gridspec' : False, 
                               'location' : "bottom",
                              'label' : "Emissions"})
    plt.ylabel("State")
    plt.yticks(rotation=0)

    save(outputfile)


def reorder(overlap, overlap_cell, cols, custom_states=None):
    """
    Get previous state name that has max enrichment
    rename any custom states
    """

    gen = pandas.read_csv(overlap, sep='\t')
    gen.rename(columns={'state (Emission order)':"state"}, inplace=True)
    gen = gen[gen['state']!="Base"]
    skip_cols = ['state', 'Genome %', 'stretch', 'intermediate']
    applygen = [col for col in gen.columns if not any([string in col for string in skip_cols])]
    gen['max_enrich'] = gen[applygen].idxmax(axis=1).str.replace(f"{overlap_cell}.","").str.replace(".bed","")
    gen['state'] = gen['state'].map(lambda x: f"E{x}")

    if custom_states is not None:
        gen['name'] = gen.apply(lambda x: custom_states[x['state']] if x['state'] in custom_states.keys() else x['max_enrich'], axis=1)
    else:
        gen['name'] = gen['max_enrich']

    gen = pandas.merge(gen, cols, how="inner", on="name")
    print(gen)
    gen['state_num'], gen['name'] = zip(*gen['name'].map(lambda x: x.split('_', 1)))
    gen['state_num'] = gen['state_num'].astype(int)
    gen['name'] = gen['name'].str.replace("Active_enhancer_1","Active_enhancer")
    
    gen.sort_values('state_num', inplace=True)

    
    my_order = gen['state'].map(lambda x: int(x.replace("E",""))).tolist()
    gen = gen[['state','Genome %','max_enrich','state_num','name','color']]

    return gen, my_order


if __name__ == '__main__':
    
    args = getOpts()

    # color infor
    cols = pandas.read_csv(args.color, sep='\t')
    
    segment_files = glob.glob(os.path.join(args.segment_dir, "*segments.bed"))
    overlap = args.overlap_enrich
    model = args.model
    mdir = args.reorder_dir
    prefix = args.prefix
    custom_states = args.custom_states
    reorder_files_dir = args.reorder_files_dir
    if not os.path.exists(reorder_files_dir):
        os.makedirs(reorder_files_dir)
    else:
        print("WARNING: FILE DIR EXISTS. Check workflow")
    # Reorder states:
    gen, my_order = reorder(overlap, args.overlap_enrich_cell, cols, custom_states = custom_states)
    print("reordered info")
    print(gen)
    
    # Output track file and reorderd files by state:
    for segment in segment_files:
        cell = os.path.basename(segment).replace("_sgements.bed","").rsplit("_")[0]
        outputfile = gp(mdir, prefix, f"{cell}.dense.bed")

        reordered_bed = make_track_bed(segment, gen, outputfile)
        get_files_by_state(reordered_bed, cell, args.reorder_files_dir)

    # Emissions heatmap
    makeHeatmap(model, gp(mdir, prefix, "emissions.pdf"), my_order)
    
    # Output info:
    gen.reset_index(inplace=True)
    gen['index'] = gen.index + 1

    print("fixing state numbers")
    print(gen)
    
    gen[['state','index','Genome %','name','color']].to_csv(gp(mdir, prefix, "reorder.dat"),
                                                    sep='\t', index=False)
