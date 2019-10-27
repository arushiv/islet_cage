workflow="nhgri_gwas_enrichment_in_tcs"
snakedir="$BASE_DIR/analysis/${workflow}"
configdir="${snakedir}/configs"
scriptdir="${snakedir}/scripts"
logdir_prune="$BASE_DIR/work/${workflow}/r2_0.2_EUR_pruning/logs"
mkdir -p $logdir_prune

# make config
python ${scriptdir}/mkconfig.py --base ${BASE_DIR} --email ${email} --config ${configdir}/config.yaml --workflow ${workflow}

# Prune and prep GWAS data
# # print workflow
snakemake -nprs ${scriptdir}/Snakefile_prune --rulegraph --configfile ${configdir}/config.yaml | dot -Tsvg > ${configdir}/${workflow}_prune.svg

# Submit pruning jobs
snakemake --cluster-config ${configdir}/cluster.yaml \
		  --cluster "sbatch --time {cluster.time} --mem {cluster.mem} --cpus-per-task {cluster.cpus} --job-name {cluster.jobname} -o {cluster.output} -e {cluster.error}  --parsable "  \
		  -j 60 --latency-wait 400 -prs ${scriptdir}/Snakefile_prune --configfile ${configdir}/config.yaml $1


logdir_gregor="$BASE_DIR/work/${workflow}/gregor/logs"
mkdir -p $logdir_gregor

# Run GWAS enrichment
snakemake -nprs ${scriptdir}/Snakefile_GREGOR --rulegraph --configfile ${configdir}/config_gregor.yaml | dot -Tsvg > ${configdir}/${workflow}_gregor.svg

# Submit jobs
snakemake --cluster-config ${configdir}/cluster.yaml \
		  --cluster "sbatch --time {cluster.time} --mem {cluster.mem} --cpus-per-task {cluster.cpus} --job-name {cluster.jobname} -o {cluster.output} -e {cluster.error}  --parsable "  \
		  -j 60 --latency-wait 400 -prs ${scriptdir}/Snakefile_GREGOR --configfile ${configdir}/config_gregor.yaml $1
