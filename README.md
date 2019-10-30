This repository contains code to reproduce results of the manuscript: 
0;95;0c## [Integrating Enhancer RNA signatures with diverse omics data identifies characteristics of transcription initiation in pancreatic islets](https://www.biorxiv.org/content/10.1101/812552v1)
	
Each directory in `analysis` contains code for analyses for different of the paper. Everything is run using [snakemake](http://snakemake.readthedocs.io/en/latest/) version 5.5.0. The analysis directories follow this general pattern:
```
├── run.sh : (file notes base directory and paths, generates a workflow config and can be used to execute analysis or print a dry run) 
├── configs
│   ├── cluster.yaml : Cluster job specifications (SLURM)
│   ├── config.yaml : Workflow configuration 
└── scripts : Scripts for analyses
    ├── script1.py
    ├── script2.R
    └── Snakefile : Snakemake files(s) 
```

Most software required can be set up by a conda environment. Conda can be obtained through the Anaconda/Miniconda Python3 distribution. These instructions are for the Linux platform

### Using conda enviroment: Install [Anaconda3](https://conda.io/docs/user-guide/install/index.html)
Assuming that you have a 64-bit system, on Linux, download and install Anaconda 3
```
$ wget https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh
$ bash Anaconda3-5.0.1-Linux-x86_64.sh
```
Answer yes to the user agreement; go with the default installation path or specify your own. Answer yes to prepend the install location to your PATH.
Please manually install [GREGOR](https://genome.sph.umich.edu/wiki/GREGOR), required to compute enrichment of GWAS in regulatory annotations. Edit the path to the GREGR.pl script file in `env/env_vars.sh`. For atac-seq, bwa is and bwa hg19 index are to be specified in `env/env_vars.sh`.
	
### Prepare analysis directory
Clone this repository and change into it.
Download the data archive from Zenodo at data/
	 	
### Set up conda environment
```
conda env create --name cage --file env/cage.yaml
conda activate cage
```
	
### Set other environment variables
#### 1. Fill up file `env/env_vars.sh` specifying email, manually installed software paths etc.
#### 2. Add variables to conda environment 
```
mkdir -p $CONDA_PREFIX/etc/conda/activate.d
mkdir -p $CONDA_PREFIX/etc/conda/deactivate.d

cp env/env_vars.sh $CONDA_PREFIX/etc/conda/activate.d/
cp env/env_vars.sh $CONDA_PREFIX/etc/conda/deactivate.d/
```
#### or directly add lines `env/env_vars.sh` to your bashrc
#### or run everytime
```
bash env/env_vars.sh
```

### Analyses order
#### Dry run of <analysis_name>
```
bash analysis/<analysis_name> run.sh -n
```
#### Run analyses by submitting jobs
```
bash analysis/<analysis_name> run.sh
```
#### Recommended order or analyses
call_tcs,
atac_seq,
annotations,
compare_with_fantom,
footprint_enrichment_in_tcs,
nhgri_gwas_enrichment_in_tcs,
roadmap_compare,
starr-seq,
tc_enrichment_in_annotations
