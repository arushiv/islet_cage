import os
import pandas
import numpy
import subprocess as sp
import glob
import re
import argparse

def getOpts():
    parser = argparse.ArgumentParser(description="""Organize NHGRI GWAS""")
    parser.add_argument('--gwasfile', required=True, help="""NHGRI GWAS file """)
    parser.add_argument('--ancestry', required=True, type=str, help="""Ancestry to subset for. Eg EUR """)
    parser.add_argument('--minN', type=int, help="""Select traits with atleast these many lead SNPs """)
    parser.add_argument('--output_full', required=True,  help="""Full output file name.""")
    parser.add_argument('--output_snpfile', required=True,  help="""Output file name.""")
    parser.add_argument('--output_reference_table', required=True,  help="""Output file name for full table.""")
    
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    
    args = getOpts()

    d = pandas.read_csv(args.gwasfile, sep='\t',
                        usecols=['DATE ADDED TO CATALOG', 'PUBMEDID', 'FIRST AUTHOR', 'DATE', 'JOURNAL',
                                 'STUDY', 'LINK', 'DISEASE/TRAIT', 'INITIAL SAMPLE SIZE',
                                 'REPLICATION SAMPLE SIZE', 'CHR_ID', 'CHR_POS', 'SNPS',
                                 'MERGED', 'RISK ALLELE FREQUENCY', 'P-VALUE', 'PVALUE_MLOG',
                                 'OR or BETA', '95% CI (TEXT)','MAPPED_TRAIT']).drop_duplicates()
    d.dropna(subset=['SNPS'], axis=0, inplace=True)

    """Subest for ancestry"""

    d = d[d['INITIAL SAMPLE SIZE'].str.contains(args.ancestry)]

    nd = pandas.DataFrame(d.groupby(['DISEASE/TRAIT'])['DISEASE/TRAIT'].size())
    traits = nd[nd['DISEASE/TRAIT'] >= args.minN]['DISEASE/TRAIT'].index.tolist()
    d = d[d['DISEASE/TRAIT'].isin(traits)]

    d.rename(columns={'SNPS' : 'SNP', 'CHR_ID' : 'chrom', 'P-VALUE' : 'P', 'DISEASE/TRAIT' : 'trait'}, inplace=True)

    d.loc[:,'SNP'] = d['SNP'].map(lambda x: re.split(';|,', x)[0])
    d.loc[:,'SNP'] = d['SNP'].map(lambda x: x.rstrip())


    d.loc[:, 'trait'] = d['trait'].map(lambda x: re.sub(r'/.+', '', x))
    d.loc[:, 'trait'] = d['trait'].map(lambda x: re.sub(r',.+', '', x))
    d.loc[:, 'trait'] = d['trait'].map(lambda x: re.sub(r'\(.+\)', '', x))
    
    d.loc[:, 'trait'] = d['trait'].str.replace("Body mass index", "BMI")
    keys = ['Hip circumference', 'Waist-to-hip ratio', 'Waist circumference', 'High light scatter reticulocyte',
            'Post bronchodilator FEV1', 'Platelet', 'Mean corpuscular hemoglobin', 'BMI',
            'Neutrophil', 'Eosinophil', 'Granulocyte']
    
    def fix(x):
        for key in keys:
            if x.startswith(key):
                return key
        return x
        
    d.loc[:, 'trait'] = d['trait'].map(fix)
    d.loc[:, 'trait'] = d['trait'].map(lambda x: x.rstrip())
    d.loc[:, 'trait'] = d['trait'].map(lambda x: re.sub("'|,|\(| ", "_", x))
    
    if TRAITS:
        d = d[d['trait'].isin(TRAITS)]
            
        d.to_csv(args.output_full, sep='\t', index=False)
        d[['DATE ADDED TO CATALOG', 'PUBMEDID', 'FIRST AUTHOR', 'DATE', 'JOURNAL', 'LINK', 'STUDY', 'trait', 'INITIAL SAMPLE SIZE']].drop_duplicates().to_excel(args.output_reference_table)
        d['SNP'].drop_duplicates().to_csv(args.output_snpfile, index=False, header=False)


