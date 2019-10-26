workflow="call_tcs"
snakedir="$BASE_DIR/analysis/${workflow}"
configdir="${snakedir}/configs"
logdir="$BASE_DIR/work/${workflow}/logs"
mkdir -p $logdir

# # print workflow
snakemake -nprs ${snakedir}/Snakefile --rulegraph | dot -Tsvg > ${configdir}/${workflow}.svg

# Submit jobs
snakemake --cluster-config ${configdir}/cluster.yaml \
		  --cluster "sbatch --time {cluster.time} --mem {cluster.mem} --cpus-per-task {cluster.cpus} --job-name {cluster.jobname} -o {cluster.output} -e {cluster.error}  --parsable" \
		  -j 60 -p --latency-wait 4 -prs ${snakedir}/Snakefile --use-conda $1

