workflow="tc_enrichment_in_annotations"
snakedir="$BASE_DIR/analysis/${workflow}"
configdir="${snakedir}/configs"
scriptdir="${snakedir}/scripts"
logdir="$BASE_DIR/work/${workflow}/logs"
datadir="$BASE_DIR/work/${workflow}/data"
mkdir -p $datadir
mkdir -p $logdir


ln -s $BASE_DIR/work/annotations/baseline/*.bed $datadir/.
ln -s $BASE_DIR/work/annotations/Islets.atac_peaks.bed $datadir/.
for i in `ls ${BASE_DIR}/work/chromhmm/selected_annotated_states/files_by_state/cell4_11.Islets.*bed | grep -v all_enhancer | grep -v all_promoter | grep -v stretchEnhancer`; do
	b=`basename $i | sed -e 's:cell4_11.::g'`;
	ln -s $i $datadir/$b;
done

# make config
python ${scriptdir}/mkconfig.py --base ${BASE_DIR} --email ${email} --config ${configdir}/config.yaml --workflow ${workflow}

# # print workflow
snakemake -nprs ${scriptdir}/Snakefile_GAT --rulegraph --configfile ${configdir}/config.yaml | dot -Tsvg > ${configdir}/${workflow}.svg

# Submit jobs
snakemake --cluster-config ${configdir}/cluster.yaml \
		  --cluster "sbatch --time {cluster.time} --mem {cluster.mem} --cpus-per-task {cluster.cpus} --job-name {cluster.jobname} -o {cluster.output} -e {cluster.error}  --parsable "  \
		  -j 60 --latency-wait 400 -prs ${scriptdir}/Snakefile_GAT --configfile ${configdir}/config.yaml $1


