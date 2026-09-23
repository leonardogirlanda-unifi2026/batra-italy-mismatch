# batra 12S primer assessment for amphibian eDNA in Italy

This repository contains the data, settings and scripts supporting the in silico and empirical assessment of the `batra` 12S primer pair for eDNA-based monitoring of amphibians in Italy. It provides the study outputs and a transparent workflow that can be adapted to another primer pair or regional taxon list.

The workflow has two components:

1. an in silico assessment of primer--template mismatches in mitochondrial records available through NCBI Nucleotide;
2. an empirical application to riverine eDNA samples from two Natura 2000 sites in north-western Italy.

The released scripts preserve the principal computational steps. Sequence inspection, alignment and curation were completed manually in Geneious Prime; they are described below because they remain necessary steps when reproducing or adapting the workflow.

## Study outputs

| Measure | Value |
| --- | ---: |
| Target taxa | 50 |
| NCBI accession occurrences retrieved | 781 (762 unique accessions) |
| Curated mitochondrial 12S records retained | 285 |
| Taxa assessed for primer mismatches | 32 |
| Unique sequence variants | 85 |
| Maximum PrimerMiner penalty score | 59.75 |
| Paired-end empirical libraries | 62 |
| Raw read pairs | 2,083,452 |

The 32 taxa assessed in silico comprise 28 native taxa and four allochthonous taxa naturalized in Italy. Five are endemic to Italy. All evaluated taxa had maximum penalty scores below the PrimerMiner threshold associated with likely primer failure.

## Repository layout

```text
.
├── Scripts/                         # in silico workflow commands
├── data/                            # primers, target list, accession lists and taxonomic overrides
├── results/                         # screening, taxonomy, variants and PrimerMiner outputs
└── empirical/
    ├── analysis/                    # Barque configuration and primer definition
    ├── reference_database/          # record-level manifest of the assignment database
    ├── results/                     # final site-level ASV table
    ├── raw_reads_manifest.tsv       # per-file read metadata and checksums
    └── raw_reads_summary.tsv         # read totals by library role
```

## In silico primer assessment

### Target taxa and nomenclature

[`data/species_list_50.txt`](data/species_list_50.txt) contains the 50 amphibian taxa documented as naturally occurring or naturalized in Italy. The list was compiled from the national checklist of the Italian fauna, the Italian IUCN Red List of Vertebrates and the Union list of invasive alien species.

[`data/taxon_name_overrides.tsv`](data/taxon_name_overrides.tsv) records the historical combinations included in sequence retrieval. It keeps the query name and accepted name separate where a nomenclatural change could otherwise hide relevant NCBI records.

### Primer definition

[`data/Batra_primers.fasta`](data/Batra_primers.fasta) contains the `batra` primers used throughout the workflow:

```text
Forward: ACACCGCCCGTCACCCT
Reverse: GTAYACTTACCATGTTACGACTT
```

### Retrieve mitochondrial records

[`Scripts/01_ncbi_download.sh`](Scripts/01_ncbi_download.sh) queries NCBI Nucleotide separately for each taxon. The query retrieves mitochondrial records between 50 and 30,000 bp that either contain a 12S-related annotation or are 5,000--30,000 bp long. This second condition retains mitochondrial genomes that may not be indexed with a 12S annotation.

The query operates on assembled NCBI Nucleotide records. It does not search raw reads deposited only in the Sequence Read Archive.

The retrieved accession occurrences are listed in [`data/accessions_initial_781.txt`](data/accessions_initial_781.txt).

### Screen, curate and dereplicate sequences

[`Scripts/02_crabs_insilico_pcr.sh`](Scripts/02_crabs_insilico_pcr.sh) screens the retrieved records with CRABS using the `batra` primer pair and an error value of 4.5. [`Scripts/03_fetch_full_sequences.sh`](Scripts/03_fetch_full_sequences.sh) retrieves the corresponding full records.

The retained records were then aligned and inspected manually in Geneious Prime. Sequences were excluded from mismatch scoring when they lacked the complete `batra` amplicon or either primer-binding region. Records with primer-binding mismatches inconsistent with other sequences of the same species were also excluded as probable sequencing or annotation errors.

The retained accessions are listed in [`data/accessions_final_285.txt`](data/accessions_final_285.txt). The following files document the screening outcomes:

- [`results/species_screening_summary.tsv`](results/species_screening_summary.tsv): one mutually exclusive outcome for each target taxon;
- [`results/insilico_filtering_results/species_no_batra_amplicon.txt`](results/insilico_filtering_results/species_no_batra_amplicon.txt): taxa without a predicted `batra` amplicon;
- [`results/insilico_filtering_results/species_incomplete_primer_sites.txt`](results/insilico_filtering_results/species_incomplete_primer_sites.txt): taxa represented only by incomplete primer-binding sites;
- [`results/insilico_filtering_results/species_missing_no_sequences.txt`](results/insilico_filtering_results/species_missing_no_sequences.txt): taxa without a retrieved assembled record;
- [`results/insilico_filtering_results/species_no_unambiguous_sequence.txt`](results/insilico_filtering_results/species_no_unambiguous_sequence.txt): taxa for which no record could be attributed unambiguously;
- [`results/insilico_filtering_results/accessions_discarded_seq.txt`](results/insilico_filtering_results/accessions_discarded_seq.txt): accessions removed during manual inspection.

[`Scripts/04_assign_tax.sh`](Scripts/04_assign_tax.sh) assigns taxonomy to the curated records with CRABS and the NCBI taxonomy files. The taxonomic table is [`results/batra_taxonomy.tsv`](results/batra_taxonomy.tsv).

[`Scripts/05_per_species_derep.sh`](Scripts/05_per_species_derep.sh) dereplicates sequences within species with VSEARCH. [`Scripts/06_variants_report.sh`](Scripts/06_variants_report.sh) produces the per-species summary in [`results/variants_report.tsv`](results/variants_report.tsv). The 285 retained records represent 85 unique sequence variants across 32 taxa.

### Score primer--template mismatches

[`Scripts/07_primerminer_eval.R`](Scripts/07_primerminer_eval.R) evaluates the forward and reverse primer-binding regions with PrimerMiner. For the alignment used in this study, forward-primer positions were 1--17 and reverse-primer positions were 76--98. These coordinates are specific to this alignment and must be recalculated for a different marker or alignment.

The released results are:

- [`results/mismatch_analysis_results/Batra_F_eval.tsv`](results/mismatch_analysis_results/Batra_F_eval.tsv);
- [`results/mismatch_analysis_results/Batra_R_eval.tsv`](results/mismatch_analysis_results/Batra_R_eval.tsv);
- [`results/mismatch_analysis_results/Table1_mismatch_summary.tsv`](results/mismatch_analysis_results/Table1_mismatch_summary.tsv), the data underlying Table 1.

## Empirical eDNA application

### Sequencing data and workflow settings

The field dataset contains 62 paired-end libraries: 48 field-sample libraries, eight field blanks, three PCR-negative controls and three positive controls. [`empirical/raw_reads_manifest.tsv`](empirical/raw_reads_manifest.tsv) provides library role, site code, read direction, filename, read count and SHA-256 checksum for each FASTQ file. [`empirical/raw_reads_summary.tsv`](empirical/raw_reads_summary.tsv) provides the corresponding totals by library role.

Raw reads were processed with Barque v1.8.5. [`empirical/analysis/barque_config_BATRA.sh`](empirical/analysis/barque_config_BATRA.sh) contains the study configuration, and [`empirical/analysis/primers.csv`](empirical/analysis/primers.csv) contains the primer and assignment settings. The processing includes trimming, primer removal, read merging, chimera removal, dereplication, denoising and taxonomic assignment. ASVs detected in negative controls were removed with microDecon.

### Metabarcoding assignment database

[`empirical/reference_database/reference_database_manifest.tsv`](empirical/reference_database/reference_database_manifest.tsv) describes the amphibian reference records used for taxonomic assignment. It reports taxon labels, record identifiers, source, public GenBank accession where available, sequence length and public-equivalent information for in-house records.

The working reference database contained 94 record occurrences: 91 public GenBank records representing 90 unique accessions, and three in-house records. The manifest documents the reference database at record level; it does not distribute the working FASTA file. This assignment database is broader than the Italy-focused in silico assessment because it reflects the records used during empirical sequence assignment.

### Final taxon-by-site table

The final post-decontamination ASV table is available as both [`empirical/results/INNATURA_ASV_table_corrected.tsv`](empirical/results/INNATURA_ASV_table_corrected.tsv) and [`empirical/results/INNATURA_ASV_table_corrected.xlsx`](empirical/results/INNATURA_ASV_table_corrected.xlsx). It reports the taxonomic assignments aggregated by Natura 2000 site.

## Adapting the workflow to another marker

1. Create a taxon list appropriate to the study area and document any historical taxonomic names needed for sequence retrieval.
2. Replace the primer sequences in `data/Batra_primers.fasta` and update the CRABS command in `Scripts/02_crabs_insilico_pcr.sh`.
3. Adapt the NCBI query in `Scripts/01_ncbi_download.sh` to the target marker and expected record lengths.
4. Run the retrieval and in silico PCR steps, then inspect alignments manually to confirm that each retained sequence spans the complete amplicon and both primer-binding sites.
5. Assign taxonomy, dereplicate within taxa and update the PrimerMiner coordinates for the new alignment before scoring primer mismatches.
6. Record the fate of every target taxon and release the accession lists, curation criteria and mismatch outputs alongside the manuscript.

## Software

The in silico workflow uses Entrez Direct, CRABS, MAFFT, Geneious Prime, VSEARCH, R and PrimerMiner. The empirical workflow uses Barque v1.8.5, Trimmomatic v0.36, FLASH v1.2.11, VSEARCH v2.27 and microDecon.

## Raw-read access

The raw FASTQ files are available from the corresponding author upon reasonable request. The repository provides their filenames, library roles, read counts and SHA-256 checksums so that requested files can be checked against the dataset used in the study.
