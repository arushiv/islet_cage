library(ggplot2)
library(cluster)
library(dplyr)
library(reshape2)
library(gplots)
library(stringr)

args <- commandArgs(TRUE)

cell_seq = c('E017',
 'E002',
 'E008',
 'E001',
 'E015',
 'E014',
 'E016',
 'E003',
 'E024',
 'E020',
 'E019',
 'E018',
 'E021',
 'E022',
 'E007',
 'E009',
 'E010',
 'E013',
 'E012',
 'E011',
 'E004',
 'E005',
 'E006',
 'E062',
 'E034',
 'E045',
 'E033',
 'E044',
 'E043',
 'E041',
 'E042',
 'E040',
 'E037',
 'E048',
 'E038',
 'E047',
 'E029',
 'E031',
 'E035',
 'E051',
 'E050',
 'E036',
 'E032',
 'E046',
 'E030',
 'E026',
 'E049',
 'E025',
 'E023',
 'E052',
 'E055',
 'E056',
 'E059',
 'E061',
 'E057',
 'E058',
 'E028',
 'E027',
 'E054',
 'E053',
 'E112',
 'E093',
 'E071',
 'E074',
 'E068',
 'E069',
 'E072',
 'E067',
 'E073',
 'E070',
 'E082',
 'E081',
 'E063',
 'E100',
 'E108',
 'E107',
 'E089',
 'E090',
 'E083',
 'E104',
 'E095',
 'E105',
 'E065',
 'E078',
 'E076',
 'E103',
 'E111',
 'E092',
 'E085',
 'E084',
 'E109',
 'E106',
 'E075',
 'E101',
 'E102',
 'E110',
 'E077',
 'E079',
 'E094',
 'E099',
 'E086',
 'E088',
 'E097',
 'E087',
 'E080',
 'E091',
 'E066',
 'E098',
 'E096',
 'E113',
 'E114',
 'E115',
 'E116',
 'E117',
 'E118',
 'E119',
 'E120',
 'E121',
 'E122',
 'E123',
 'E124',
 'E125',
 'E126',
 'E127',
 'E128',
 'E129')

name_seq = c('IMR90_fetal_lung_fibroblasts_Cell_Line',
 'ES-WA7_Cells',
 'H9_Cells',
 'ES-I3_Cells',
 'HUES6_Cells',
 'HUES48_Cells',
 'HUES64_Cells',
 'H1_Cells',
 'ES-UCSF4__Cells',
 'iPS-20b_Cells',
 'iPS-18_Cells',
 'iPS-15b_Cells',
 'iPS_DF_6.9_Cells',
 'iPS_DF_19.11_Cells',
 'H1_Derived_Neuronal_Progenitor_Cultured_Cells',
 'H9_Derived_Neuronal_Progenitor_Cultured_Cells',
 'H9_Derived_Neuron_Cultured_Cells',
 'hESC_Derived_CD56+_Mesoderm_Cultured_Cells',
 'hESC_Derived_CD56+_Ectoderm_Cultured_Cells',
 'hESC_Derived_CD184+_Endoderm_Cultured_Cells',
 'H1_BMP4_Derived_Mesendoderm_Cultured_Cells',
 'H1_BMP4_Derived_Trophoblast_Cultured_Cells',
 'H1_Derived_Mesenchymal_Stem_Cells',
 'Primary_mononuclear_cells_from_peripheral_blood',
 'Primary_T_cells_from_peripheral_blood',
 'Primary_T_cells_effector/memory_enriched_from_peripheral_blood',
 'Primary_T_cells_from_cord_blood',
 'Primary_T_regulatory_cells_from_peripheral_blood',
 'Primary_T_helper_cells_from_peripheral_blood',
 'Primary_T_helper_cells_PMA-I_stimulated',
 'Primary_T_helper_17_cells_PMA-I_stimulated',
 'Primary_T_helper_memory_cells_from_peripheral_blood_1',
 'Primary_T_helper_memory_cells_from_peripheral_blood_2',
 'Primary_T_CD8+_memory_cells_from_peripheral_blood',
 'Primary_T_helper_naive_cells_from_peripheral_blood',
 'Primary_T_CD8+_naive_cells_from_peripheral_blood',
 'Primary_monocytes_from_peripheral_blood',
 'Primary_B_cells_from_cord_blood',
 'Primary_hematopoietic_stem_cells',
 'Primary_hematopoietic_stem_cells_G-CSF-mobilized_Male',
 'Primary_hematopoietic_stem_cells_G-CSF-mobilized_Female',
 'Primary_hematopoietic_stem_cells_short_term_culture',
 'Primary_B_cells_from_peripheral_blood',
 'Primary_Natural_Killer_cells_from_peripheral_blood',
 'Primary_neutrophils_from_peripheral_blood',
 'Bone_Marrow_Derived_Cultured_Mesenchymal_Stem_Cells',
 'Mesenchymal_Stem_Cell_Derived_Chondrocyte_Cultured_Cells',
 'Adipose_Derived_Mesenchymal_Stem_Cell_Cultured_Cells',
 'Mesenchymal_Stem_Cell_Derived_Adipocyte_Cultured_Cells',
 'Muscle_Satellite_Cultured_Cells',
 'Foreskin_Fibroblast_Primary_Cells_skin01',
 'Foreskin_Fibroblast_Primary_Cells_skin02',
 'Foreskin_Melanocyte_Primary_Cells_skin01',
 'Foreskin_Melanocyte_Primary_Cells_skin03',
 'Foreskin_Keratinocyte_Primary_Cells_skin02',
 'Foreskin_Keratinocyte_Primary_Cells_skin03',
 'Breast_variant_Human_Mammary_Epithelial_Cells_(vHMEC)',
 'Breast_Myoepithelial_Primary_Cells',
 'Ganglion_Eminence_derived_primary_cultured_neurospheres',
 'Cortex_derived_primary_cultured_neurospheres',
 'Thymus',
 'Fetal_Thymus',
 'Brain_Hippocampus_Middle',
 'Brain_Substantia_Nigra',
 'Brain_Anterior_Caudate',
 'Brain_Cingulate_Gyrus',
 'Brain_Inferior_Temporal_Lobe',
 'Brain_Angular_Gyrus',
 'Brain_Dorsolateral_Prefrontal_Cortex',
 'Brain_Germinal_Matrix',
 'Fetal_Brain_Female',
 'Fetal_Brain_Male',
 'Adipose_Nuclei',
 'Psoas_Muscle',
 'Skeletal_Muscle_Female',
 'Skeletal_Muscle_Male',
 'Fetal_Muscle_Trunk',
 'Fetal_Muscle_Leg',
 'Fetal_Heart',
 'Right_Atrium',
 'Left_Ventricle',
 'Right_Ventricle',
 'Aorta',
 'Duodenum_Smooth_Muscle',
 'Colon_Smooth_Muscle',
 'Rectal_Smooth_Muscle',
 'Stomach_Smooth_Muscle',
 'Fetal_Stomach',
 'Fetal_Intestine_Small',
 'Fetal_Intestine_Large',
 'Small_Intestine',
 'Sigmoid_Colon',
 'Colonic_Mucosa',
 'Rectal_Mucosa_Donor_29',
 'Rectal_Mucosa_Donor_31',
 'Stomach_Mucosa',
 'Duodenum_Mucosa',
 'Esophagus',
 'Gastric',
 'Placenta_Amnion',
 'Fetal_Kidney',
 'Fetal_Lung',
 'Ovary',
 'Pancreatic_Islets',
 'Fetal_Adrenal_Gland',
 'Placenta',
 'Liver',
 'Pancreas',
 'Lung',
 'Spleen',
 'A549_EtOH_0.02pct_Lung_Carcinoma_Cell_Line',
 'Dnd41_TCell_Leukemia_Cell_Line',
 'GM12878_Lymphoblastoid_Cells',
 'HeLa-S3_Cervical_Carcinoma_Cell_Line',
 'HepG2_Hepatocellular_Carcinoma_Cell_Line',
 'HMEC_Mammary_Epithelial_Primary_Cells',
 'HSMM_Skeletal_Muscle_Myoblasts_Cells',
 'HSMM_cell_derived_Skeletal_Muscle_Myotubes_Cells',
 'HUVEC_Umbilical_Vein_Endothelial_Primary_Cells',
 'K562_Leukemia_Cells',
 'Monocytes-CD14+_RO01746_Primary_Cells',
 'NH-A_Astrocytes_Primary_Cells',
 'NHDF-Ad_Adult_Dermal_Fibroblast_Primary_Cells',
 'NHEK-Epidermal_Keratinocyte_Primary_Cells',
 'NHLF_Lung_Fibroblast_Primary_Cells',
 'Osteoblast_Primary_Cells')



makePlot = function(d, cols){
    print(head(d))
    p <- ggplot(d, aes(x=factor(id), y=Standardized_Epigenome_name)) +
        geom_tile(aes(fill=state)) + 
        scale_fill_manual(values=cols) + 
        theme(axis.text = element_text(size=5), 
              panel.background = element_rect(fill = 'white', colour = 'black'), 
              axis.text.x=element_blank(),
              axis.ticks.x = element_blank()) +
        labs(x="Segments", y="Human Epigenomes")
        
    return(p)
}

get_clust_order = function(d){
    d2 <- data.frame(d[,-1], row.names=d[,1])
    m1 = as.matrix(d2)
    class(m1) <- "numeric"

    gower.dist <- daisy(m1, metric = c("gower"))  
    aggl.clust.c <- hclust(gower.dist, method = "complete")
    return(aggl.clust.c)
    }


run_clust_plot = function(filename, color_file){
                                        # Get state colors
    c = read.table(color_file, header=T, sep='\t')
    state_seq = c$state #c('1_TssA','2_TssAFlnk','3_TxFlnk','4_Tx','5_TxWk','6_EnhG','7_Enh','8_ZNF/Rpts','9_Het','10_TssBiv','11_BivFlnk','12_EnhBiv','13_ReprPC','14_ReprPCWk','15_Quies')
    cols = rgb(c$red, c$green, c$blue, maxColorValue = 255)

    # read main data
    d = read.table(filename, header=T, sep='\t')

    # Remove E039 as it is a duplicate of E038
    d = d[d$cell != "E039",]
    
    d$feature = paste(d$chrom, d$start, d$end, sep="_")
    d = d[complete.cases(d), ] 

    # Prep to get clusters
    d1 <- dcast(d[,c('feature','Standardized_Epigenome_name','state_num')], feature ~ Standardized_Epigenome_name, value.var = "state_num")

    # get x axis order by clustering
    x_order = get_clust_order(d1)$order

    # match x order with feature names after clustering
    d1$id = rownames(d1)
    d1 = d1[,c('feature','id')]
    d = merge(d, d1)


    d$id = factor(d$id, levels = x_order)
    d$state = factor(d$state, levels = state_seq)
    d$Standardized_Epigenome_name = factor(d$Standardized_Epigenome_name, levels=rev(name_seq))
    

    myplot = makePlot(d, cols)
    
    return(myplot)
}




myplot = run_clust_plot(args[1], args[2])


pdf(paste(args[3], ".pdf", sep=""), height=10, width=7)
print(myplot)
dev.off()


png(paste(args[3], ".png", sep=""), height=10, width=7, unit="in", res=300)
print(myplot)
dev.off()
