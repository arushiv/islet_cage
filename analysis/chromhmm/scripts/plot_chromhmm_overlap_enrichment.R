library(ggplot2)
library(reshape2)
library(dplyr)
library(tidyr)
library(stringr)

args <- commandArgs(TRUE)
d <- read.table(snakemake@input[['overlap_enrich']], header=T, sep='\t')

d = d[d$state..Emission.order. != "Base",]
d1 = melt(d, id.vars = c("state..Emission.order.","Genome.."), variable.name = c('PNAS.2017'), value.name = "enrichment")
d1$PNAS.2017 = gsub(".bed", "", d1$PNAS.2017)


d1[,c('cell','PNAS_state')] = str_split_fixed(d1$PNAS.2017, "\\.", 2)

head(d1)
names(d1)[names(d1) == 'state..Emission.order.'] <- 'newState'

d1 = d1[! d1$PNAS_state %in% c("intermediateEnhancer","stretch4_2kbEnhancer","stretch6kbEnhancer"), ]

d1$PNAS_state <- factor(d1$PNAS_state, levels = c("1_Active_TSS","2_Weak_TSS","3_Flanking_TSS","5_Strong_transcription","6_Weak_transcription","8_Genic_enhancer","9_Active_enhancer_1","10_Active_enhancer_2","11_Weak_enhancer","14_Bivalent_poised_TSS","16_Repressed_polycomb","17_Weak_repressed_polycomb","18_Quiescent_low_signal","stretchEnhancer","typicalEnhancer"))

colvector <- c(rgb(255,0,0,maxColorValue=255),rgb(255,69,0,maxColorValue=255),rgb(255,69,0,maxColorValue=255),rgb(0,128,0,maxColorValue=255),rgb(0,100,0,maxColorValue=255),rgb(194,225,5,maxColorValue=255),rgb(255,195,77,maxColorValue=255),rgb(255,195,77,maxColorValue=255),rgb(255,255,0,maxColorValue=255),rgb(205,92,92,maxColorValue=255),rgb(128,128,128,maxColorValue=255),rgb(192,192,192,maxColorValue=255),rgb(255,255,255,maxColorValue=255),rgb(246,139,30,maxColorValue=255), rgb(242,233,83,maxColorValue=255))


makeplot <- function(d){
    p <- ggplot(d, aes(x=PNAS_state, y=enrichment)) +
        geom_point(aes(fill = PNAS_state), shape=21, size=3) +
        geom_line(aes(colour = cell, group=cell)) +
        theme(axis.text.x = element_text(size = 8, angle = 90, hjust=1, vjust=0.5),
              panel.background = element_rect(fill = 'white', colour = 'black'),
              panel.grid.major = element_line(colour = 'grey', size=0.1, linetype="dashed"),
              plot.title = element_text(size = 14),
              axis.title.x = element_text(size=12),
              axis.title.y = element_text(size=12),
              legend.background = element_rect(fill="white")) +
        facet_wrap(~ newState, scales = "free_y", nrow=4) +
        scale_fill_manual(values=colvector, guide=FALSE) + 
        labs(x = "State assignment for Islets for PNAS 2017", y="Fold Enrichment")
    return(p)
}

pdf(snakemake@output[['fig']], height=10, width=10)
makeplot(d1)    
dev.off()



