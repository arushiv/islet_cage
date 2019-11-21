This repository contains code to run analyses presented in the manuscript: 
## [Integrating Enhancer RNA signatures with diverse omics data identifies characteristics of transcription initiation in pancreatic islets](https://www.biorxiv.org/content/10.1101/812552v1)
	
Directories in the `analysis` folder contain individual workflows, run using [snakemake](http://snakemake.readthedocs.io/en/latest/) version 5.5.0. Config for a SLURM cluster execution are provided. The analysis directories follow this general pattern:
```
├── run.sh : for workflow execution
├── configs
│   ├── cluster.yaml : Cluster job specifications (SLURM)
│   └── config.yaml : Workflow configuration (created from mkconfig.py while using environment variables)
└── scripts : Scripts for analyses
    ├── mkconfig.py
    ├── script1.py
    ├── script2.R
    └── Snakefile : Snakemake files(s) 
```
Given the correct environment variables are set and the input data is downloaded from Zenodo (see below), executing the `run.sh` file sets base directory and paths, generates a workflow config and can be used to execute analysis or print a dry run). Most software required can be set up by a conda environment. Conda can be obtained through the Anaconda/Miniconda Python3 distribution. These instructions are for the Linux platform:

### 1. Set up conda and software:
#### Install [Anaconda3](https://conda.io/docs/user-guide/install/index.html) if you don't already have conda on your system.
#### Please manually install [GREGOR](https://genome.sph.umich.edu/wiki/GREGOR), required to compute enrichment of GWAS in regulatory annotations. Edit the path to the GREGR.pl script file in `env/env_vars.sh`.
#### For atac-seq, bwa and bwa hg19 index are to be specified in `env/env_vars.sh`.
#### For MPRA analysis, install R package [MPRAnalyze version 1.3.1](https://rdrr.io/github/YosefLab/MPRAnalyze/) which is currently available from github
```
install.packages("remotes")
remotes::install_github("YosefLab/MPRAnalyze")
```
### 2. Prepare analysis directory
Clone this repository and change into it.
Download the data archive from the [Zenodo deposition](https://zenodo.org/record/3524578#.XdbDaL97l7O) and untar the archive
```
tar -xvzf islet-cage-zenodo.tar.gz
```
	 	
### 3. Set up conda environment
#### 1. Fill up file `env/env_vars.sh` specifying email, manually installed software paths etc.
```
conda env create --name cage --file env/cage.yaml
conda activate cage
mkdir -p $CONDA_PREFIX/etc/conda/activate.d
mkdir -p $CONDA_PREFIX/etc/conda/deactivate.d

cp env/env_vars.sh $CONDA_PREFIX/etc/conda/activate.d/
cp env/env_vars.sh $CONDA_PREFIX/etc/conda/deactivate.d/
```

### Analyses 
#### Dry run of <analysis_name>
```
analysis/<analysis_name>/run.sh -n
```
#### Run analyses by submitting jobs
```
analysis/<analysis_name>/run.sh
```
