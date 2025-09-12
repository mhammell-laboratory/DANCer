#!/bin/env Rscript

# This is a script to preprocess vst transformed counts to eigengenes 

## Check for input files. Require sample VST file and eigengene RData
args = commandArgs(trailingOnly=T)
if(length(args)<2){
    stop("Usage: Rscript eigengene_calculation.R [VST file] [eigengene RData]",call.=FALSE)
}

vstfile = args[1]
base = basename(args[1])
base = tools::file_path_sans_ext(base)
Rdata = args[2]

## Loading Eigengene information
library(WGCNA)
load(file = Rdata)

## Load and process VST file
vstcounts = read.table(vstfile,header=T,row.names=1,sep="\t")
vst_filtered = vstcounts[rownames(vstcounts) %in% names(moduleLabels),]

if(dim(vst_filtered)[1] < length(moduleColors)){
    missing_genes <-  names(moduleLabels[-which(names(moduleLabels) %in% row.names(vstcounts))])
    print(paste(length(missing_genes), " genes are missing from the ALS subtype sc pseudobulk classifier gene model, they will be replaced with the minimum input count value. The replacement constititutes ", length(missing_genes)/length(moduleLabels)*100, "% of the total gene model. Consider this in interpretation of results.", sep=""))
    fill <- as.data.frame(matrix(min(vstcounts),  length(missing_genes), dim(vstcounts)[2]), row.names = missing_genes)
    colnames(fill) <- colnames(vstcounts)
    vst_filled <- rbind(vstcounts, fill)
    counts_module_ordered <- vst_filled[names(moduleLabels),]
    vst_eigen <- moduleEigengenes(t(counts_module_ordered),moduleColors, grey = FALSE)
}else{
    counts_module_ordered <- vst_filtered[names(moduleLabels),]
    vst_eigen = moduleEigengenes(t(as.matrix(counts_module_ordered)),moduleColors,grey=FALSE)
}

vst_MEs = vst_eigen[["eigengenes"]]
vst_MEs$MEviolet = NULL  # Sex specific module

file = paste0(base, "_MEs.tsv")
write.table(vst_MEs,file,sep="\t",col.names=T,row.names=T,quote=F)
