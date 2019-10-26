library(CAGEr)
library(BSgenome.Hsapiens.UCSC.hg19)
library(argparse)


getOpts <- function(){
    parser <- ArgumentParser(description='Run CAGE workflow')
    parser$add_argument('--ctss',  help='CTSS file')
    parser$add_argument('--out_string', help='Output file names will start with this string')
    parser$add_argument("--norm_type", help='Normalize using c("powerLaw", "simpleTpm", "none")')
    parser$add_argument("--type_clu", help='Use  "dist" for distclu or "para" for paraclu')
    parser$add_argument("--tpm_singleton", type="integer", help='TPm threshold to consider singleton TCs')
    parser$add_argument("--tpm", type="integer", help='TPm threshold to consider CTSSs')
    args <- parser$parse_args()
    return(args)
}


args = getOpts()
print(args)
## n_cage_paths <- list.files("/lab/work/arushiv/erna_analyses/nisc_exploreQTL_parameters/intermediateFiles/analyses_cager/directional_sample_r1ss/", full.names = TRUE)
n_cage_path = args$ctss
n_cage_sample = gsub(".ctss", "", paste("s_", basename(args$ctss), sep=""))

n_CAGEset <- new("CAGEset", genomeName = "BSgenome.Hsapiens.UCSC.hg19", inputFiles = n_cage_path, inputFilesType = "ctss", sampleLabels = n_cage_sample)

getCTSS(n_CAGEset)

cairo_pdf(paste(args$out_string, ".qc_plots.pdf", sep=""), height=8, width=8)
plotReverseCumulatives(n_CAGEset, fitInRange = c(5, 1000), onePlot = TRUE)
print("Reverse cumulatives plotted")
dev.off()

normalizeTagCount(n_CAGEset, method = args$norm_type, alpha = 1.02, T = 1*10^6)
print(paste("CAGE tags normalized using norm = ", args$norm_type, sep=""))

## exportCTSStoBedGraph(n_CAGEset, values = "normalized", format = "BigWig")
## print("Track bigWig files created")

print("Making tag clusters")
if (args$norm_type == "none"){
    thresholdIsTpm = FALSE
} else {
    thresholdIsTpm = TRUE
}



clusterCTSS(object = n_CAGEset,
            threshold = args$tpm,
            thresholdIsTpm = thresholdIsTpm,
            nrPassThreshold = 1,
            method = paste(args$type_clu, "clu", sep=""),
            removeSingletons = TRUE,
            keepSingletonsAbove = args$tpm_singleton,
            reduceToNonoverlapping = TRUE,
            maxDist = 20,
            useMulticore = TRUE,
            nrCores = 4)

print(paste("Tag clusters made after norm = ", args$norm_type, "using method = ", args$type_clu, "clu", sep=""))


tc <- tagClusters(n_CAGEset, sample = n_cage_sample)

tcname = paste(args$out_string, ".bed", sep = "")
write.table(tc, file = tcname, quote = FALSE, na = "NA", sep='\t', row.names = FALSE)
print("Tag clusters saved")
