library(ggplot2)
library(reshape2)
library(scales)
library(dplyr)
library(gtools)
library(stringr)


args <- commandArgs(TRUE)
d <- read.table(args[1], header=T)


makePointPlot <- function(d, xstring, ystring){

    mine <- min(d$minuslog10pval, na.rm=TRUE)
    maxe <- max(d$minuslog10pval, na.rm=TRUE)
    vector <- c(mine, mine + 0.33*(maxe-mine), mine + 0.66*(maxe-mine), maxe)
    
    p <- ggplot(d, aes_string(y = ystring, x = xstring)) +
        geom_point(aes(fill=minuslog10pval), colour="black", shape=21) +
        geom_text(aes(label=overlap), size=3) +
        theme(text = element_text(size=8),
              strip.text.y= element_text(size=10),
              strip.text.x=element_text(size=9),
              axis.text.x = element_text(size=7),
              axis.text.y = element_text(size=8),
              panel.background = element_rect(fill="white", colour="black"),
              legend.key.size=unit(3, "mm"),
              panel.grid.major.y=element_line(colour="grey", size=0.3),
              panel.grid.major.x=element_line(colour="grey", size=0.15),
              legend.position="bottom",
              legend.text=element_text(angle=90, hjust=1, vjust=0.5),
              axis.title.y = element_blank()) +
        scale_fill_gradientn(name="-log10(p value)", values=rescale(vector), colours=c("white","pink","red","darkred"), breaks=round(vector,2), labels=round(vector,2)) +
        labs(y="GWAS fold enrichment", x="Trait", scales="free_x") +
        coord_flip() +
        geom_hline(yintercept=1, color="blue", alpha=0.5, linetype="dashed") 
    return(p)
}

d <- d[d$overlap >= 1,]
d <- d[d$pval <= 1,]

bonferroni_threshold <- (0.05)

d$foldEnrichment <- d$overlap/d$expected_overlap
d$log2_foldEnrichment <- log2(d$overlap/d$expected_overlap)
d$minuslog10pval <- -log10(d$pval)


d$trait = gsub("_", "\n", d$trait)
d$trait = gsub("RheumatoidArthritis","Rheumatoid Arthritis",d$trait)
d$trait = gsub("T2D","type 2 diabetes\n(NHGRI)",d$trait)
d$trait = gsub("FGlu","Fasting Glucose",d$trait)
d$trait = gsub("diamante_T2D","type 2 diabetes\n(DIAMANTE)",d$trait)

## d$trait <- factor(d$trait, levels = c('Fasting\nGlucose','type 2\ndiabetes','Rheumatoid Arthritis'))


## ## SUBSET Point PLOT
pdf(args[2], height=6, width=5)
makePointPlot(d, "trait", "foldEnrichment")
dev.off()
