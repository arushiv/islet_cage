library(MPRAnalyze)
library(argparse)
library(ggplot2)
library(BiocParallel)

getOpts <- function(){
    parser <- ArgumentParser(description='Analyze MPRA data')
    parser$add_argument('--rna',  help='RNA counts file')
    parser$add_argument('--dna',  help='DNA counts file')
    parser$add_argument('--rna_annot',  help='RNA annot file')
    parser$add_argument('--dna_annot',  help='DNA annot file')
    parser$add_argument('--size_norm', action="store_true",  help='DNA annot file')
    parser$add_argument('--output', help='Output file name')
    args <- parser$parse_args()
    return(args)
}

args = getOpts()

dna = data.matrix(read.table(args$dna, sep='\t', header=T, row.names="refname"))
rna = data.matrix(read.table(args$rna, sep='\t', header=T, row.names="refname"))

dna_annot = read.table(args$dna_annot, sep='\t', header=T, row.names="bcnum")
rna_annot = read.table(args$rna_annot, sep='\t', header=T, row.names="bcnum_rep")


obj = MpraObject(dnaCounts = dna, rnaCounts = rna, dnaAnnot = dna_annot, rnaAnnot = rna_annot)

if (args$size_norm == TRUE) {
    obj <- estimateDepthFactors(obj, which.lib = "dna",
                                depth.estimator = "uq")
    obj <- estimateDepthFactors(obj, lib.factor = c("rep"),
                                which.lib = "rna",
                                depth.estimator = "uq")
}

obj = analyzeQuantification(obj = obj, dnaDesign = ~ barcode, rnaDesign = ~ rep)

write.table(testEmpirical(obj), args$output, quote=FALSE, sep='\t')       


