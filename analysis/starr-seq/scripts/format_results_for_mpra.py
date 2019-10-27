
# coding: utf-8

import pandas
import numpy
import sys
import os
import argparse

def getOpts():
    parser = argparse.ArgumentParser(description="""Format data for MPRAnalyze""")
    parser.add_argument('--results', required=True, help="""Result file""")
    parser.add_argument('--pool', nargs='+', required=True, help="""pool""")
    parser.add_argument('--config', required=True, help="""config""")
    parser.add_argument('--minDNA', type=int, required=True, help="""minDNA""")
    parser.add_argument('--split_ref_alt', action="store_true", help="""Format to include ref or alt as covariates""")
    parser.add_argument('--out_prefix', required=True, help="""Output prefix""")
    args = parser.parse_args()
    
    return args


def assign_barcode_num(d):
    d = d.reset_index().reset_index()
    d.drop(['index'], axis=1, inplace=True)
    
    return d


def fix_ref_alt_count(d):
    d_ref = d[d.index.str.contains("ref")].add_suffix('_ref')
    d_alt = d[d.index.str.contains("alt")].add_suffix('_alt')
    d_ref.index = d_ref.index.str.replace("_ref", "")
    d_alt.index = d_alt.index.str.replace("_alt", "")
    dout = pandas.concat([d_ref, d_alt], axis=1)
    return dout


def fix_ref_alt_annot(d):
    newinfo_ref = d.copy()
    newinfo_alt = d.copy()
    
    newinfo_ref.rename(lambda x: f"{x}_ref", inplace=True)
    newinfo_ref['allele'] = "ref"
    
    newinfo_alt.rename(lambda x: f"{x}_alt", inplace=True)
    newinfo_alt['allele'] = "alt"
    
    dout = pandas.concat([newinfo_ref, newinfo_alt])
    return dout

                                                        
def format_rna(bm_df, split_ref_alt):
    ctype = "rna"
    new = bm_df.groupby('refname').apply(assign_barcode_num)
    new.rename(columns = {'level_0': 'bcnum'}, inplace=True)
    new['bcnum'] = new['bcnum'].map(lambda x: f"b{x}")
   
    new.drop(['refname'], axis=1, inplace=True)
    new.reset_index(inplace=True)
    new.drop('level_1', axis=1, inplace=True)
    newm = new.melt(id_vars=['refname', 'bcnum', 'barcode'], var_name='rep', value_name=ctype)
    newm['bcnum_rep'] = newm.apply(lambda x: f"{x['bcnum']}_{x['rep']}", axis=1)
    
    info = newm[['bcnum_rep']].drop_duplicates()
    info[['barcode', 'rep']] = info['bcnum_rep'].str.split('_', expand=True)
    info.set_index('bcnum_rep', inplace=True)
    
    format_df = newm[['refname','bcnum_rep',ctype]].pivot_table(index='refname', columns='bcnum_rep', values=ctype, fill_value=0)

    if split_ref_alt:
        format_df = fix_ref_alt_count(format_df)
        info = fix_ref_alt_annot(info)
        format_df.rename(columns={'bcnum_rep':'refname'}, inplace=True)
    return info, format_df


def format_dna(bm_df, split_ref_alt):
    ctype = "dna"
    new = bm_df.groupby('refname').apply(assign_barcode_num)
    new.rename(columns = {'level_0': 'bcnum'}, inplace=True)
    new['bcnum'] = new['bcnum'].map(lambda x: f"b{x}")
   
    new.drop(['refname'], axis=1, inplace=True)
    new.reset_index(inplace=True)
    new.drop('level_1', axis=1, inplace=True)
    
    info = new[['bcnum']].drop_duplicates()
    info['barcode'] = info['bcnum']
    info.set_index('bcnum', inplace=True)
    info['lib'] = "dna"
    format_df = new[['refname','bcnum',ctype]].pivot_table(index='refname', columns='bcnum', values=ctype, fill_value=0)

    if split_ref_alt:
        format_df = fix_ref_alt_count(format_df)
        info = fix_ref_alt_annot(info)
        format_df.rename(columns={'bcnum':'refname'}, inplace=True)
    return info, format_df


def format_data(d, pool, config, split_ref_alt):
    bm = d[(d['pool'].isin(pool)) & (d['config']==config)][['barcode','refname','rep1','rep2','rep3','dna']]
    bm_rna = bm[['barcode','refname','rep1','rep2','rep3']]
    assert not bm_rna.empty
    
    # for DNA df
    bm_dna = bm[['barcode','refname','dna']]
    assert not bm_dna.empty
    
    dna_info, dna_counts = format_dna(bm_dna, split_ref_alt)
    rna_info, rna_counts = format_rna(bm_rna, split_ref_alt)
    
    return dna_info, rna_info, dna_counts, rna_counts


def convert_int(d, exclude):
    cols = [c for c in d.columns if c != exclude]
    for c in cols:
        d[cols] = d[cols].astype(int) 
    return d


if __name__ == '__main__':

    args = getOpts()
    
    d = pandas.read_csv(args.results, sep='\t')

    d = d[d['minDNA'] == args.minDNA]

    assert not d.empty
    
    dna_info, rna_info, dna_counts, rna_counts = format_data(d, args.pool, args.config, args.split_ref_alt)

    print(f"Number of inserts (DNA) = {len(dna_counts.index)}")
    print(f"Number of inserts (RNA) = {len(rna_counts.index)}")

    
    rna_info.to_csv(f"{args.out_prefix}.rna_annots.tsv", sep='\t')
    dna_info.to_csv(f"{args.out_prefix}.dna_annots.tsv", sep='\t')

    if args.split_ref_alt:
        dna_counts.dropna(inplace=True)
        rna_counts.dropna(inplace=True)

        dna_counts = convert_int(dna_counts, "bcnum")
        rna_counts = convert_int(rna_counts, "bcnum_rep")
    
        print(f"Number of inserts with both ref and alt qualifying (DNA) = {len(dna_counts.index)}")
        print(f"Number of inserts with both ref and alt qualifying (RNA) = {len(rna_counts.index)}")

        rna_counts.to_csv(f"{args.out_prefix}.rna_counts.tsv", sep='\t', index_label="refname")
        dna_counts.to_csv(f"{args.out_prefix}.dna_counts.tsv", sep='\t', index_label="refname")

    else:
        rna_counts.to_csv(f"{args.out_prefix}.rna_counts.tsv", sep='\t')
        dna_counts.to_csv(f"{args.out_prefix}.dna_counts.tsv", sep='\t')

