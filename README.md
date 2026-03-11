# Technical Assessment of the Batra 12S Primer for Italian Amphibians

This repository contains the workflow, scripts, and datasets used to evaluate the performance of the **Batra 12S primer pair** (Valentini et al., 2016) for Italian amphibian eDNA metabarcoding.

The assessment combines:

- reference database curation
- in silico PCR screening
- primer–template mismatch analysis
- taxonomic validation
- sequence dereplication and variant analysis
- mismatch scoring using PrimerMiner

The objective is to evaluate the **technical feasibility of applying the Batra marker to Italian amphibian communities**.


# Workflow Overview

The analysis was conducted in the following steps.


## 1. Reference Sequence Retrieval
 
`Scripts/01_ncbi_download.sh`

A list of **53 Italian amphibian taxa** (native + invasive or potentially invasive species) was used to retrieve mitochondrial **12S sequences from NCBI** using Entrez Direct (`esearch`).

Search filters:

- mitochondrial records annotated as **12S rRNA**
- sequence length filter to exclude nuclear fragments

### Output

`data/accessions_initial_919.txt`  
919 sequences belonging to **50 species**

`results/insilico_filtering_results/species_missing_no_sequences.txt`  
Species from the initial target list for which **no suitable 12S sequences were retrieved from NCBI**


## 2. In Silico PCR (CRABS)
  
`Scripts/02_crabs_insilico_pcr.sh`

Sequences were screened using **CRABS** to retain only those predicted to amplify with the **Batra primer pair**:

`Batra_Forward:
ACACCGCCCGTCACCCT
Batra_Reverse:
GTAYACTTACCATGTTACGACTT`


Default CRABS mismatch threshold

### Output
  
415 sequences belonging to **36 species**

`results/insilico_filtering_results/species_no_batra_amplicon.txt`  
Species represented in the initial dataset whose sequences **did not yield a Batra amplicon** during in silico PCR


## 3. Recovery of Full Sequences
  
`Scripts/03_fetch_full_sequences.sh`

Accession numbers of the amplified sequences were extracted and re-downloaded from NCBI to obtain the **full mitochondrial sequences containing primer-binding regions**.

## 4. Manual Curation and Primer Validation

Sequences were manually inspected in **Geneious Prime (v2026.0.2)**.

Steps performed:

- primer binding tested using *Test with Saved Primers* (≤4 mismatches allowed)
- sequences aligned using **MAFFT**
- sequences trimmed to include **amplicon + primer-binding regions**

Sequences were removed if they:

- lacked complete primer-binding sites, two species were escluded this way `results/insilico_filtering_results/species_incomplete_primer_sites.txt`
- showed mismatch patterns inconsistent with other sequences of the same species, two records were discarded this way `results/insilico_filtering_results/accessions_discarded_seq.txt`

### Final curated dataset

408 sequences  
34 species

### Output

`data/accessions_final_408.txt`

`results/insilico_filtering_results/species_incomplete_primer_sites.txt`  
Species whose sequences contained the target region but **lacked complete primer-binding sites**, preventing mismatch analysis.


## 5. Taxonomic Metadata Retrieval
  
`Scripts/04_assign_tax.sh`

Taxonomic information associated with each accession number was retrieved using the **CRABS `--download-taxonomy` option** and the NCBI taxonomy database.

### Output

`results/batra_taxonomy.tsv`


## 6. Sequence Dereplication
  
`Scripts/05_per_species_derep.py`

Sequences were:

- grouped by species
- dereplicated using **VSEARCH (`--derep_fulllength`)**

### Output

100 unique sequence variants  
34 species


## 7. Variant Report
  
`Scripts/06_variants_report.sh`

Summary of sequence variants per species.

### Output

`resultrs/variants_report.tsv`


## 8. Primer Mismatch Analysis
  
`Scripts/07_primerminer_eval.R`

Primer mismatch scoring was performed using **PrimerMiner** in R.

Penalty score interpretation (Elbrecht & Leese 2017):

| Penalty score | Interpretation |
|---------------|---------------|
| >120 | likely primer failure |
| <60 | compatible with amplification |

### Results

Maximum observed penalty score: **59.75**

No systematic accumulation of mismatches near the **3′ primer termini** was detected.

### Output

- `results/mismatch_analysis_results/Batra_F_eval.tsv`
- `results/mismatch_analysis_results/Batra_R_eval.tsv`
- `results/mismatch_analysis_results/Table1_mismatch_summary.tsv`


# Key Results

- 919 sequences retrieved from the initial NCBI query (50 species)
- 415 sequences predicted to amplify the **Batra region**
- 408 curated sequences retained after manual inspection
- 34 species included in the final mismatch analysis

Species composition:

- **28 native species** (4 endemic to Italy)
- **6 invasive or potentially invasive species**

Additional findings:

- most mismatch variation occurred in the **reverse primer-binding region**
- only two species showed mismatches near the **3′ end** (position 5 from the 3' end)
- no species exceeded the functional mismatch threshold


# Repository Structure

```
.
├── scripts/
│   ├── 01_ncbi_download.sh
│   ├── 02_crabs_insilico_pcr.sh
│   ├── 03_fetch_full_sequences.sh
│   ├── 04_assign_tax.sh
│   ├── 05_per_species_derep.py
│   ├── 06_variants_report.sh
│   └── 07_primerminer_eval.R
│
├── data/
│   ├── Batra_primers.fasta
│   ├── accessions_amplicons_408.txt
│   ├── accessions_manually_discarded.txt
│   ├── accessions_initial_919.txt
│   ├── evaluated_species_34.txt
│   └── species_list_53.txt
│
├── results/
│   ├── in_silico_filtering_results/
│   │   ├── species_incomplete_primer_sites.txt
│   │   ├── species_missing_no_sequences.txt
│   │   ├── species_no_batra_amplicon.txt
│   │   ├── mismatch_analysis_results/
│   │   │   ├── Batra_F_eval.tsv
│   │   │   ├── Batra_R_eval.tsv
│   │   │   ├── Table1_mismatch_summary.tsv
│   ├── batra_taxonomy.tsv
│   └── variants_report.tsv
├── .gitignore
├── LICENSE
└── README.md
```
# Software Requirements

- Entrez Direct (NCBI E-utilities)  
  https://www.ncbi.nlm.nih.gov/books/NBK179288/

- CRABS ≥ 0.2.0

- VSEARCH ≥ 2.21.1

- Geneious Prime 2026.0.2  
  https://www.geneious.com

- R ≥ 4.0

Required R packages:

- PrimerMiner
- Biostrings


# Citation

If you use this workflow, please cite:

Elbrecht V, Leese F (2017) PrimerMiner: an R package for development and in silico validation of DNA metabarcoding primers. *Ecol Evol* 8:622–626. https://doi.org/10.1111/2041-210X.12687

Jeunen GJ et al. (2023) CRABS: a software program to generate curated reference databases for metabarcoding sequencing data. *Mol Ecol Resour* 23:725–738. https://doi.org/10.1111/1755-0998.13741

R Core Team (2021) R: A language and environment for statistical computing. https://www.R-project.org/

Rognes T et al. (2016) VSEARCH: a versatile open source tool for metagenomics. *PeerJ* 4:e2584. https://doi.org/10.7717/peerj.2584

Valentini A et al. (2016) Next-generation monitoring of aquatic biodiversity using environmental DNA metabarcoding. *Mol Ecol* 25:929–942. https://doi.org/10.1111/mec.13428
