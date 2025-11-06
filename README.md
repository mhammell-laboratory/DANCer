# Deep layer ALS Neural network Classifier (DANCer)
Version 1.0.1

DANCer takes RNA-seq data from postmortem ALS cortex tissues and classifies them to the three ALS molecular subtypes described in [Tam et al 2019](https://pubmed.ncbi.nlm.nih.gov/31665631/). This is achieved by converting variance stabilized transformed (VST) counts data to WGCNA module eigengene values, then running them through a trained neural network for ALS subtype assignment. For more details, please refer to the publication in the citation section.

DANCer is designed for bulk RNA-seq datasets, while scDANCer is designed for pseudo-bulk single-cell/single-nuclei RNA-seq datasets.

Created by Kat O'Neill & Molly Gale Hammell, January 2022

Copyright (C) 2022-2024 Kat O'Neill & Molly Gale Hammell

Website: [Molly Gale Hammell lab](https://www.mghlab.org/software)

Contact: mghcompbio@gmail.com

## Installation

### Install miniconda
```
$ wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
$ bash Miniconda3-latest-Linux-x86_64.sh
```

### Install dependencies
```
$ git clone https://github.com/mhammell-laboratory/DANCer.git
$ cd DANCer
$ conda env create -f environment.yaml
```

## Usage

### DANCer
1. Activate the `DANCer` conda environment
```
$ conda activate DANCer
```
2. Calculate eigengene values from VST counts.
   - The VST file can be generated using DESeq2 (install separately).
   - Usage: `Rscript eigengene_calculation.R [VST file] [eigengene RData]`
   - This will generate an output file (`[file basename]_MEs.tsv`). In the example below, it would be `input_vstCounts_MEs.tsv`.
```
$ Rscript DANCER/scripts/eigengene_calculation.R input_vstCounts.txt DANCER/datafiles/DANCer_WGCNA_moduleInfo.RData
```
3. Run the neural net classifier
   - Usage: `python DANCer_predict.py  [file with eigenvalues] [model weights]`
   - This will generate an output file (`[file basename]_classifier_out.tsv`). In the example below, it would be `input_vstCounts_MEs_classifier_out.tsv`.
```
$ python DANCER/scripts/DANCer_predict.py input_vstCounts_MEs.tsv DANCER/datafiles/DANCer_weights.hdf5
```
4. Process the output to get human-readable classification
   - Usage: `sh process_DANCer_output.sh [DANCer output]`
   - This will generate an output file (`[prefix]_classification.txt`). In the example below, it would be `input_vstCounts_MEs_classification.txt`.
```
$ sh DANCER/scripts/process_DANCer_output.sh input_vstCounts_MEs_classifier_out.tsv
```

### scDANCer
1. Activate the `DANCer` conda environment
```
$ conda activate DANCer
```
2. Pseudo-bulk the single-cell/single-nuc RNA-seq data
   - This step will differ depending on the program used to quantify expression from your scRNA/snRNA-seq. The example below is uses a Cell Ranger output and `bedtools groupBy` to generate a pseudobulk count for a library:
```
$ gunzip -cf cellranger_output/count/filtered_feature_bc_matrix/features.tsv.gz | awk -v OFS="<tab>" '{print NR,$2}' | sort -k1,1 > featureIndex.txt
$ gunzip -cf cellranger_output/count/filtered_feature_bc_matrix/matrix.mtx.gz | sed '1,3d;s/ /<tab>/g' | cut -d "<tab>" -f 2- | sort -k1,1 | join -t "<tab>" -j 1 featureIndex.txt - | sort -k2,2 | groupBy -g 2 -c 3 -o sum > pseuobulk_counts.txt
```
3. Generate a combined pseudobulk count matrix for all libraries and generate a VST count file
4. Calculate eigengene values from VST counts
   - Usage: `Rscript eigengene_calculation.R [VST file] [eigengene RData]`
   - This will generate an output file (`[file basename]_MEs.tsv`). In the example below, it would be `pseudobulk_vstCounts_MEs.tsv`.
```
$ Rscript scDANCER/scripts/eigengene_calculation.R pseudobulk_vstCounts.txt scDANCER/datafiles/scDANCer_WGCNA_moduleInfo.RData
```
5. Run the neural net classifier
   - Usage: `python scDANCer_predict.py  [file with eigenvalues] [model weights]`
   - This will generate an output file (`[file basename]_classifier_out.tsv`). In the example below, it would be `pseudobulk_vstCounts_MEs_classifier_out.tsv`.
```
$ python scDANCER/scripts/scDANCer_predict.py pseudobulk_vstCounts_MEs.tsv scDANCER/datafiles/scDANCer_weights.hdf5
```
6. Process the output to get human-readable classification
   - Usage: `sh process_scDANCer_output.sh [scDANCer output]`
   - This will generate an output file (`[prefix]_classification.txt`). In the example below, it would be `pseudobulk_vstCounts_MEs_classification.txt`.
```
$ sh scDANCER/scripts/process_scDANCer_output.sh pseudobulk_vstCounts_MEs_classifier_out.tsv
```

## Copying and distribution
DANCer is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with DANCer. If not, see [this website](http://www.gnu.org/licenses/).

## Citation
O'Neill K, Shaw R, Bolger I, NYGC ALS Consortium, Tam OH, Phatnani H, Gale Hammell M. (2025) ALS molecular subtypes are a combination of cellular and pathological features learned by deep multiomics classifiers. Cell Rep. PMID: [40067829](https://pubmed.ncbi.nlm.nih.gov/40067829/)
