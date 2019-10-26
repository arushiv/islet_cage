library(ggplot2)
library(stringr)

args = commandArgs(TRUE)

make_genome_perc = function(f){
    
    p = ggplot(f, aes(x=col, y=as.factor(index))) +
    geom_tile(fill="white", color="black") +
    geom_text(aes(label=genome)) + 
    theme(axis.title=element_blank(),
          axis.ticks.y=element_blank(),
          axis.text.y=element_blank(),
          panel.background=element_blank())
    
    return(p)
    }

make_chromState_colors = function(f){
    p = ggplot(f, aes(x=annot, y=as.factor(index))) +
    geom_tile(aes(fill=as.factor(index)), color="black") +
    scale_fill_manual(values=colvector) +
    geom_text(aes(label=name)) + 
    theme(text=element_text(size=8),
        axis.title=element_blank(),
         axis.ticks.y=element_blank(),
         axis.text.y=element_blank(),
        axis.text.x=element_text(size=8),
        panel.background=element_blank()
         )+
    guides(fill=FALSE)
    return(p)
    }

statefile = args[1]

f = read.table(statefile, sep='\t', header=T)
f$col = "Genome %"
f$annot = "Chromatin state"
f$genome = round(f$Genome.., 3)
n = length(unique(f$index))
f$index = factor(f$index, levels=rev(seq(1, n, 1)))
f$name = gsub("_", " ", f$name)

f[, c('r', 'g','b')] = str_split_fixed(f$color, ",", 3)
colvector = rev(rgb(f$r, f$g, f$b, maxColorValue = 255))
head(f)

pdf(args[2], height=7, width=1.5)
make_genome_perc(f)
dev.off()


pdf(args[3], height=7, width=3)
make_chromState_colors(f)
dev.off()





