
library(ggplot2)
library(scales)


order_all = c('Active TSS',
              'ATAC-seq peaks',
              'Flanking TSS',
              'Genic enhancer',
              'Bivalent poised TSS',
              'Active enhancer',
              'Strong transcription',
              'Weak TSS',
            'Weak enhancer',
 'Weak transcription',
 'Repressed polycomb',
              'Quiescent low signal',
 "5' UTR (UCSC)",
 'TSS (Hoffman)',
 'Coding (UCSC)',
 'Promoter (UCSC)',
 'H3K4me3 peaks (Trynka)',
 'H3K9ac peaks (Trynka)',
 'FetalDHS (Trynka)',
 'Conserved (LindbladToh)',
 'TFBS ENCODE',
 'H3K9ac (Trynka)',
 'DHS peaks (Trynka)',
 'H3K4me3 (Trynka)',
 'DHS (Trynka)',
 "3' UTR (UCSC)",
 'DGF ENCODE',
  'Enhancer (Hoffman)',
 'H3K27ac PGC2',
 'SuperEnhancer (Hnisz)',
 'H3K27ac (Hnisz)',
 'H3K4me1 (Trynka)',
 'H3K4me1 peaks (Trynka)',
 'PromoterFlanking (Hoffman)',
 'Enhancer (Andersson)',
 'WeakEnhancer (Hoffman)',
'Intron (UCSC)',
 'CTCF (Hoffman)',
  'Transcribed (Hoffman)',
'Repressed (Hoffman)')

select = c('Active TSS',
              'ATAC-seq peaks',
              'Flanking TSS',
              'Genic enhancer',
              'Bivalent poised TSS',
              'Active enhancer',
              'Strong transcription',
              'Weak TSS',
               'Weak enhancer',
 'Weak transcription',
 'Repressed polycomb',
              'Quiescent low signal',
 "5' UTR (UCSC)",
 'Coding (UCSC)',
 'Promoter (UCSC)',
 'H3K4me3 peaks (Trynka)',
 'H3K9ac peaks (Trynka)',
 'Conserved (LindbladToh)',
 'TFBS ENCODE',
 'DHS peaks (Trynka)',
 'H3K4me3 (Trynka)',
 "3' UTR (UCSC)",
 'SuperEnhancer (Hnisz)',
 'H3K4me1 peaks (Trynka)',
 'Enhancer (Andersson)',
 'Intron (UCSC)')

cols <- c("Significant (Bonferroni)" ="#ff7f00",
          'Nominally significant' = "#4daf4a",
          'non-significant' = "#377eb8")

 
makeplot = function(d){
    p = ggplot(d, aes(x=annotation, y=l2fold)) + 
    geom_point(aes(color=significance), shape=16, size=2.5) + 
    geom_errorbar(aes(ymin=fold_cilo, ymax=fold_cihigh)) + 
    theme_bw() +
    theme(legend.position="bottom") + 
    scale_colour_manual(values = cols) +
    geom_hline(yintercept=0) +
    coord_flip() + 
    labs(y="log2(Fold enrichment)", x="") +
    guides(colour = guide_legend(nrow = 3))
    return(p)
}


d = read.csv("/lab//work/arushiv/cage/work/tc_enrichment_in_annotations/results_GAT_formatted.dat", header=T, sep='\t')
d$fold_cilo = log2(d$observed/(d$CI95high))
d$fold_cihigh = log2(d$observed/(d$CI95low))


d$annotation = factor(d$annotation, levels=rev(order_all))
d$significance = factor(d$significance, levels=c("Significant (Bonferroni)", 
                                                     "Nominally significant",
                                                    "non-significant"))
pdf("/lab//work/arushiv/cage/work/tc_enrichment_in_annotations/figures/fig.ordered_errorbars.pdf",
   height=10, width = 5)
makeplot(d)
dev.off()




d1 = d[d$annotation %in% select,]

d1$annotation = factor(d1$annotation, levels=rev(select))
d1$significance = factor(d1$significance, levels=c("Significant (Bonferroni)", 
                                                     "Nominally significant",
                                                    "non-significant"))
pdf("/lab//work/arushiv/cage/work/tc_enrichment_in_annotations/figures/fig.subset_ordered_errorbars.pdf",
   height=6, width = 3.5)
makeplot(d1)
dev.off()


