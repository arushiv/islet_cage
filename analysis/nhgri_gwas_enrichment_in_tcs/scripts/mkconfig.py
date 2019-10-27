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

CHROM = range(1, 23)
gregor_config = config
for chrom in CHROM:
    vcfLink = f"ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr{chrom}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz"
    indexLink = f"ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr{chrom}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz.tbi"
    cmd = f'wget {vcfLink} --directory-prefix={BASE_DIR}/data/1000GenomesDownloads/ ;  wget {indexLink} --directory-prefix={BASE_DIR}/data/1000GenomesDownloads/'
    sp.check_output(cmd, shell=True)

config.update({
    # prune
    'population_type': "Superpopulation code",  # Choose which column in vcf_sampleInfo file to subset samples on. Another option could be "Population code" to subest by population
    'population_code': "EUR",
    'prune_r2' : 0.2,
    '1000g_maf' : 0.05, # Min MAF in popluation considered to avoid ultra low freq alleles that result in duplicate rsIDs due to which plink fails
    'DATA': {
        'nhgri_gwas': get_path("data/gwas/gwas_catalog_v1.0.2-associations_e92_r2018-05-29.tsv"),
        '1000g' : get_path("data/1000GenomesDownloads/ALL.chr{chrom}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz"),
        '1000g_index' : get_path("data/1000GenomesDownloads/ALL.chr{chrom}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz.tbi"),
        'vcf_sampleInfo' : get_path("data/1000GenomesDownloads/igsr_3990samples_allPopulations.tsv"),
    },
    'scripts':{
        'gwas_nhgri': get_path("analysis/nhgri_gwas_enrichment_in_tcs/scripts/get_GWAS.py")
    }
})

name = config_file.replace(".yaml", "")
gregor_config_file = f"{name}_gregor.yaml"
gregor_config.update({
    # From of output dir name for each trait.
    'output_dir' : "output_{trait}.ld{gregor_r2}",
    'DATA' :{
        'input_snps' : get_path("work/nhgri_gwas_enrichment_in_tcs/r2_0.2_EUR_pruning/pruned_snps/pruned.{trait}.txt"),
        'annotation' : get_path("work/call_tcs/tcs/tissue_tcs_formatted/{annotation}.bed"),
        'ANNOTATIONS' : "expand(config['DATA']['annotation'], annotation = ['tc_paraclu.Islets.tpmThresh2singletonThresh2.minExpIn10.noblacklist'])",
        'output' : "enrichment_stats.txt",
        'output_fig' : "fig.gwas_enrichment_tcs.pdf"
    },
    'PARAMETERS' : {
        'gregor_version_path' : os.getenv('GREGOR'),
        'TRAITS' : "glob_wildcards(config['DATA']['input_snps'])[0]",
        'config_name' : "enrich.{trait}.ld{gregor_r2}.conf",
        'POPULATION' : "EUR",
        'gregor_r2' : 0.8,
        'cores': 10,
        'nameFieldSeparator': '.',
        'jobFieldSeparator': '.',
        'header' : "trait ld r2 tc_type tissue tpmThresh minExpIn tc_filter  overlap expected_overlap pval"
    },
    'SCRIPTS' :{
        'makeConfFile' : get_path("analysis/nhgri_gwas_enrichment_in_tcs/scripts/gregor_makeConf.py"),
        'assembleDF' : get_path("analysis/nhgri_gwas_enrichment_in_tcs/scripts/makeDataFrame_gregor_new.py"),
        'plot' : get_path("analysis/nhgri_gwas_enrichment_in_tcs/scripts/plot_gwas_enrichment.R")
    }
})

with open(gregor_config_file, 'w+') as f:
    yaml.dump(gregor_config, f, default_flow_style=False)
                
with open(config_file, 'w+') as f:
    yaml.dump(config, f, default_flow_style=False)

        




