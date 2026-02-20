# Technical Assessment of the Batra 12S Primer for Italian Amphibians

This repository contains the full workflow, scripts, and reference datasets used to evaluate the performance of the Batra 12S primer pair (Valentini et al., 2016) for Italian amphibian eDNA metabarcoding.

The assessment combines:
-In silico primer-template mismatch analysis
-Reference database curation
-Taxonomic validation
-Sequence dereplication and variant analysis
-PrimerMiner mismatch scoring

The objective is to evaluate the technical feasibility of applying the Batra marker in an Italian context.

## Overview of the Workflow:

### 1) Reference Sequence Retrieval

01_ncbi_download.sh

53 Italian amphibian taxa (native + invasive/potentially invasive)

-12S mitochondrial sequences downloaded from NCBI using esearch

-Query restricted to mitochondrial 12S rRNA regions

-Length filter applied (not to retrieve nuclear sequences)

Output:

italian_amphibians_12S.fasta

### 2) In Silico PCR (CRABS)

02_crabs_insilico_pcr.sh

Sequences were filtered to retain only those predicted to amplify with the Batra primer pair:
```
#Batra_Forward:

ACACCGCCCGTCACCCT


#Batra_Reverse:

GTAYACTTACCATGTTACGACTT
```

Default CRABS mismatch threshold: 4.5 mismatches per primer.

Output:

batra_12S_amplicons.fasta

### 3️) Recovery of Full Sequences

03_fetch_full_sequences.sh

Accession numbers were extracted and re-downloaded to obtain full mitochondrial sequences containing primer binding sites.

Output:

batra_full_sequences.fasta

### Manual Curation and Primer Validation in Geneious Prime

Sequences were:

-uploaded and checked in Geneious Prime

-Tested for primer binding (using: "test with saved primers", ≤4 mismatches allowed)

-Aligned using MAFFT

-Trimmed to include amplicon + primer binding regions

Outlier sequences ( inconsistent mismatch patterns with all the other variants of a species) were manually removed.

Final curated dataset:

408 sequences
34 species


### 4) Taxonomic Assignment (CRABS)

04_assign_tax.sh

Taxonomy assigned using NCBI taxonomy database.

Output:

batra_taxonomy.tsv


### 5) Dereplication 

05_per_species_derep.py

Sequences were:

-Grouped by species

-Dereplicated using VSEARCH (--derep_fulllength)

Final dataset:

100 unique sequence variants for 34 species.


### 6) Variants report

06_variants_report.sh

Report file:

variants_report.tsv


### 7️) Primer Mismatch Analysis (PrimerMiner)

07_primerminer_eval.R

Mismatch scoring performed in R using PrimerMiner.

Penalty score thresholds (Elbrecht & Leese 2017):

120 → likely non-functional

<60 → compatible with amplification

Observed maximum penalty score:

59.75

No systematic 3′-terminal mismatch accumulation detected.

results: Batra_F_eval.tsv Batra_R_eval.tsv Table1_mismatch_summary.tsv


## Key Results

919 sequences retrieved (50 species)

408 curated sequences retained

34 species included in final mismatch analysis

28 native species (4 endemic)

6 invasive/potentially invasive species

Most mismatch variation occurred in the reverse primer region

Only two species showed mismatches near the 3′ end (position 5 from 3′)

No species exceeded functional mismatch thresholds

The study also generated the first complete Batra amplicon reference sequence for Rana italica, improving database completeness for future applications.

## Repository Structure
├── scripts/

│   ├── 01_ncbi_download.sh

│   ├── 02_crabs_insilico_pcr.sh

│   ├── 03_fetch_full_sequences.sh

│   ├── 04_assign_tax.sh

│   ├── 05_per_species_derep.py

│   ├── 06_variants_report.sh

│   ├── 07_primerminer_eval.R

├── data/

│   ├── Batra_primers.fasta

│   ├── accessions_amplicons_408.txt

│   ├── accessions_manually_discarded.txt

│   ├── accessions_initial_919.txt

│   ├── lista_anfibi.txt

│   ├── batra_uniqueseq_itamph.fasta

│   ├── haplotype_report.tsv

├── results/

│   ├── Batra_F_eval.tsv

│   ├── Batra_R_eval.tsv

│   ├── Table1_mismatch_summary.tsv

│   ├── variants_report.tsv

└── README.md

## Software Requirements

Entrez Direct (NCBI E-utilities)

CRABS 0.2.0 

VSEARCH v2.21.1 (Rognes et al. 2016)

Geneious Prime 2026.0.2 

R (≥4.0)

PrimerMiner

Biostrings

## Citation

If you use this workflow, please cite:

Valentini et al. 2016

Elbrecht & Leese 2017

Jeunen et al. 2023 (CRABS)
