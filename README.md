# Batra 12S primers for Italian amphibian eDNA

This repository accompanies the manuscript **“In silico and empirical assessment of the Batra 12S primers for eDNA-based monitoring of amphibians in the Italian peninsula.”** It serves three related purposes:

1. it provides the supplementary data used to document the in silico assessment and the field application;
2. it records the main analytical decisions, intermediate counts, exclusions and revision checks;
3. it provides a worked example that can be adapted to evaluate a different metabarcoding primer pair or target-taxon list.

The repository is divided into an **in silico primer-assessment workflow** and an **empirical eDNA application**. The shell, Python and R commands preserve the main operations used in the study. Manual curation steps are identified explicitly, so the repository should be read as a transparent, reproducible workflow description rather than as a single unattended pipeline.

## At a glance

| Component | Released result |
| --- | ---: |
| Target taxa in the revision list | 55 |
| Taxa evaluated in the final mismatch analysis | 34 |
| Taxa with incomplete primer-binding sites | 2 |
| Taxa with no Batra amplicon in the original in silico PCR | 14 |
| Taxa with no suitable sequence retrieved | 5 |
| Initial NCBI accession occurrences | 919 (902 unique) |
| Sequences reported after CRABS screening | 415, representing 36 taxa |
| Curated accessions retained for mismatch analysis | 408 |
| Unique sequence variants | 100 |
| Empirical paired-end libraries | 62 (124 FASTQ files) |
| Raw read pairs | 2,083,452 |
| Taxa in the released site-level ASV table | 21 (5 amphibian and 16 non-target vertebrate taxa) |
| Reads represented in the released ASV table | 236,743 |

The working revision list contains the 53 taxa used in the original retrieval plus *Hyla perrini* and *Ichthyosaura apuana*. Selected non-native or non-Italian taxa were retained as technical comparators. Their inclusion should not be interpreted as a current national distribution record or as a formal classification under invasive-alien-species legislation.

## Repository contents

```text
.
├── README.md
├── LICENSE
├── Scripts/
│   ├── 01_ncbi_download.sh
│   ├── 02_crabs_insilico_pcr.sh
│   ├── 03_fetch_full_sequences.sh
│   ├── 04_assign_tax.sh
│   ├── 05_per_species_derep.sh
│   ├── 06_variants_report.sh
│   └── 07_primerminer_eval.R
├── data/
│   ├── Batra_primers.fasta
│   ├── species_list_53.txt
│   ├── species_list_55.txt
│   ├── taxon_name_overrides.tsv
│   ├── accessions_initial_919.txt
│   ├── accessions_final_408.txt
│   └── evaluated_species_34.txt
├── results/
│   ├── species_screening_summary.tsv
│   ├── targeted_sequence_audit.tsv
│   ├── accession_flow.tsv
│   ├── review_audit_report.txt
│   ├── variants_report.tsv
│   ├── batra_taxonomy.tsv
│   ├── insilico_filtering_results/
│   └── mismatch_analysis_results/
└── empirical/
    ├── analysis/
    │   ├── barque_config_BATRA.sh
    │   └── primers.csv
    ├── reference_database/
    │   ├── BATRA_amphibian_reference_public.fasta
    │   └── reference_database_release_notes.tsv
    ├── results/
    │   ├── INNATURA_ASV_table_corrected.xlsx
    │   └── INNATURA_ASV_table_corrected.tsv
    ├── raw_reads_manifest.tsv
    ├── raw_reads_summary.tsv
    └── raw_reads_archive_SHA256.txt
```

The raw FASTQ files are distributed as a GitHub Release asset rather than being committed to the Git history. See [Raw reads and release files](#raw-reads-and-release-files).

## Part I: in silico primer assessment

### 1. Define the biological scope

The original analysis started from [`data/species_list_53.txt`](data/species_list_53.txt). The revision list in [`data/species_list_55.txt`](data/species_list_55.txt) adds *H. perrini* and *I. apuana*. Query names, accepted names and historical combinations are kept separate in [`data/taxon_name_overrides.tsv`](data/taxon_name_overrides.tsv), preventing a nomenclatural change from breaking the link to the original retrieval.

When adapting the workflow, create a one-name-per-line target list and decide in advance whether it represents:

- a verified regional checklist;
- a broader surveillance list that also includes non-native taxa;
- technical comparators used only to test primer behaviour.

These categories should be stored explicitly rather than inferred later from the results.

### 2. Retrieve assembled mitochondrial records from NCBI

[`Scripts/01_ncbi_download.sh`](Scripts/01_ncbi_download.sh) queries NCBI Nucleotide (`nuccore`) separately for each taxon and retrieves assembled mitochondrial records annotated with 12S-related terms. The original length filter was 50–30,000 bp.

Important scope limitation: this query interrogates assembled Nucleotide records. It does **not** search raw reads in the Sequence Read Archive.

For the original Batra run:

- 919 accession occurrences were downloaded;
- 902 accession numbers were unique;
- 50 target taxa were represented.

The original accessions are retained in [`data/accessions_initial_919.txt`](data/accessions_initial_919.txt).

### 3. Screen sequences by in silico PCR

[`Scripts/02_crabs_insilico_pcr.sh`](Scripts/02_crabs_insilico_pcr.sh) screens the downloaded records using CRABS and the Batra primers:

```text
Forward: ACACCGCCCGTCACCCT
Reverse: GTAYACTTACCATGTTACGACTT
```

The study reports 415 sequences representing 36 taxa after this step. The intermediate list of 415 accessions is not available in the repository; consequently, entries that are absent from both the final and manually discarded lists are labelled conservatively in [`results/accession_flow.tsv`](results/accession_flow.tsv).

Taxa for which the original screening returned no predicted Batra amplicon are listed in [`results/insilico_filtering_results/species_no_batra_amplicon.txt`](results/insilico_filtering_results/species_no_batra_amplicon.txt).

### 4. Retrieve complete records and inspect primer-binding regions

[`Scripts/03_fetch_full_sequences.sh`](Scripts/03_fetch_full_sequences.sh) retrieves the complete NCBI records corresponding to predicted amplicons. The sequences were then inspected manually in Geneious Prime 2026.0.2:

- primer binding was checked with a maximum of four mismatches;
- sequences were aligned with MAFFT;
- records were trimmed to retain the amplicon and both primer-binding regions;
- incomplete primer-binding sites were excluded from mismatch scoring;
- records with mismatch patterns inconsistent with conspecific sequences were removed as probable sequencing or annotation errors.

Two affected taxa are recorded in [`species_incomplete_primer_sites.txt`](results/insilico_filtering_results/species_incomplete_primer_sites.txt), and the two manually discarded accessions are recorded in [`accessions_discarded_seq.txt`](results/insilico_filtering_results/accessions_discarded_seq.txt).

The final accession list contains 408 records representing 34 taxa: [`data/accessions_final_408.txt`](data/accessions_final_408.txt).

### 5. Retrieve taxonomy and dereplicate within species

[`Scripts/04_assign_tax.sh`](Scripts/04_assign_tax.sh) uses CRABS and the NCBI taxonomy files to associate accessions with taxonomic names.

[`Scripts/05_per_species_derep.sh`](Scripts/05_per_species_derep.sh) then:

1. links accessions to species;
2. renames FASTA headers;
3. separates records by species;
4. dereplicates full-length sequences with VSEARCH.

The embedded Python step requires Biopython. Dereplication is performed within species, so an identical sequence occurring in two different taxa is not silently merged across taxonomic labels.

[`Scripts/06_variants_report.sh`](Scripts/06_variants_report.sh) summarizes the number of input records, unique variants and abundance of the most frequent variant for each species. The released result is [`results/variants_report.tsv`](results/variants_report.tsv).

### 6. Score primer-template mismatches

[`Scripts/07_primerminer_eval.R`](Scripts/07_primerminer_eval.R) evaluates the forward and reverse primer-binding regions with PrimerMiner. The aligned Batra dataset used forward-primer columns 1–17 and reverse-primer columns 76–98. These coordinates are specific to this alignment and must be recalculated for a different marker or alignment.

The released outputs are:

- [`Batra_F_eval.tsv`](results/mismatch_analysis_results/Batra_F_eval.tsv);
- [`Batra_R_eval.tsv`](results/mismatch_analysis_results/Batra_R_eval.tsv);
- [`Table1_mismatch_summary.tsv`](results/mismatch_analysis_results/Table1_mismatch_summary.tsv).

The maximum observed penalty score was 59.75. No taxon exceeded the score of 120 associated with likely primer failure in the PrimerMiner framework.

### 7. Document the fate of every target taxon

[`results/species_screening_summary.tsv`](results/species_screening_summary.tsv) assigns each of the 55 revision taxa to one mutually exclusive outcome:

- evaluated in the mismatch analysis;
- incomplete primer-binding sites;
- no Batra amplicon in the original in silico PCR;
- no suitable sequence retrieved.

[`results/targeted_sequence_audit.tsv`](results/targeted_sequence_audit.tsv) records the targeted revision checks for *H. perrini* and *I. apuana* and retains the original workflow outcomes for *H. sarda* and *Salamandrina perspicillata*.

## Part II: empirical eDNA application

### Sampling and laboratory overview

The field dataset comprised eight stream sampling locations within two Natura 2000 areas in north-western Italy. At each location, six 1 L water samples were collected along a 50 m transect. Field blanks were processed in parallel. DNA extractions were amplified in technical triplicate with the Batra primers, and pooled products were indexed and sequenced on an Illumina MiSeq using 2 × 150 bp reads.

The released raw-data package contains:

- 48 field-sample libraries;
- 8 field blanks;
- 3 PCR negative-control libraries;
- 3 positive-control libraries;
- 62 paired-end libraries in total;
- 2,083,452 read pairs.

The files identify the positive controls as `Pos1`, `Pos2A` and `Pos2B`. Their biological composition is not encoded in the filenames and should not be inferred from the repository.

### Bioinformatic processing

Raw reads were processed with Barque v1.8.5. The exact supplied settings are in [`empirical/analysis/barque_config_BATRA.sh`](empirical/analysis/barque_config_BATRA.sh), and the active primer/database definition is in [`empirical/analysis/primers.csv`](empirical/analysis/primers.csv).

Key settings include:

| Setting | Value |
| --- | ---: |
| Read crop length | 90 bp |
| Minimum merge overlap | 30 bp |
| Maximum merge overlap | 280 bp |
| Maximum primer differences | 2 |
| Minimum query coverage | 0.90 |
| Minimum hit length | 40 bp |
| Minimum hits in one sample | 3 |
| Minimum hits in the experiment | 5 |
| Species identity threshold | 0.99 |
| Genus identity threshold | 0.95 |
| Higher-level threshold in the primer file | 0.90 |

The Barque workflow includes Trimmomatic filtering, FLASH read merging, chimera removal, VSEARCH-based dereplication and assignment, and ASV generation. ASVs detected in negative controls were removed with microDecon using default parameters. No custom microDecon script was used.

### Empirical reference database

[`empirical/reference_database/BATRA_amphibian_reference_public.fasta`](empirical/reference_database/BATRA_amphibian_reference_public.fasta) is the public-release version of the amphibian component supplied for the empirical analysis. It contains 90 records.

Three internal records were omitted because their sequences are identical to retained public GenBank records:

- `RS3-Batr01_Bufotes-viridis` and `RS7-Batr01_Bufotes-viridis` are identical to FJ882813;
- `Rit2-Batr01_Rana-italica` is identical to PQ758684.

One exact duplicate occurrence of PP471678 was also removed. These operations do not remove a unique sequence variant. All changes are documented in [`reference_database_release_notes.tsv`](empirical/reference_database/reference_database_release_notes.tsv).

The released FASTA contains amphibian references only. Non-target vertebrate ASVs were investigated during downstream curation with BLAST; the corresponding non-target reference records are not included in this FASTA. The file should therefore not be presented as a universal vertebrate reference database.

### ASV table

The final taxon-by-site table is provided in both Excel and machine-readable TSV formats:

- [`INNATURA_ASV_table_corrected.xlsx`](empirical/results/INNATURA_ASV_table_corrected.xlsx);
- [`INNATURA_ASV_table_corrected.tsv`](empirical/results/INNATURA_ASV_table_corrected.tsv).

The public copy corrects three taxonomic labels without changing any read count:

- *Erithacus rubecula*: family Muscicapidae;
- *Parus major*: family Paridae;
- *Oncorhynchus* sp.: group Fish.

The table reports 236,743 reads assigned to 21 reportable vertebrate taxa across the eight site codes. The manuscript reports 236,763 reads after filtering, denoising and decontamination. The 20-read difference is consistent with the table note that human sequences and potential contaminants were omitted, but the unavailable per-ASV intermediate table prevents independent attribution of those 20 reads. Both totals are retained here to keep the reporting transparent.

## Raw reads and release files

The raw FASTQ files and checksum are available in the GitHub Release [`empirical-data-v1`](https://github.com/leonardogirlanda-unifi2026/batra-italy-mismatch/releases/tag/empirical-data-v1):

- `raw_reads_batra.zip` contains the 124 compressed FASTQ files, the manifest and the summary;
- `SHA256SUMS.txt` verifies the downloaded archive.

The same manifest is tracked in [`empirical/raw_reads_manifest.tsv`](empirical/raw_reads_manifest.tsv). It records library role, site code, read direction, read count and SHA-256 checksum for every FASTQ file. [`empirical/raw_reads_summary.tsv`](empirical/raw_reads_summary.tsv) provides totals by library role.

The expected SHA-256 checksum for `raw_reads_batra.zip` is also stored in [`empirical/raw_reads_archive_SHA256.txt`](empirical/raw_reads_archive_SHA256.txt).

## Adapting the workflow to another primer pair

The sequence below is the minimum recommended adaptation path.

### Parameters that must be changed

| Component | Batra example | Change for a new primer |
| --- | --- | --- |
| Target taxa | `data/species_list_55.txt` | Supply the relevant checklist and comparator categories |
| Locus search | Mitochondrial 12S terms | Replace with the target locus and known annotation synonyms |
| Record-length filter | 50–30,000 bp | Set bounds that retain complete marker and primer sites |
| Primer sequences | Batra forward/reverse | Replace in CRABS, the primer FASTA, PrimerMiner and Barque |
| In silico amplicon constraints | CRABS defaults used here | Set and report mismatch and length parameters explicitly |
| Alignment coordinates | Forward 1–17; reverse 76–98 | Recalculate from the new aligned primer-binding regions |
| Empirical crop length | 90 bp | Set below the expected merged amplicon length |
| Merge overlap | 30–280 bp | Adapt to read length and amplicon size |
| Assignment thresholds | 0.99/0.95/0.90 | Validate against the discriminatory power of the new marker |
| Reference database | Curated Batra-length references | Build a locus-specific database including expected non-targets |

### Recommended sequence of work

1. Freeze and version the target-taxon list before downloading sequences.
2. Store the query name separately from the accepted taxonomic name.
3. Record the exact database, date, query, annotation terms and length limits.
4. Preserve accession lists after retrieval, in silico PCR and manual curation.
5. Inspect both primer-binding regions; a locus annotation alone does not guarantee that the amplicon is present.
6. Dereplicate within taxon, not across taxa.
7. Recalculate alignment coordinates before running PrimerMiner.
8. Validate taxonomic assignment thresholds against closely related species.
9. Include field blanks, PCR negatives and a documented positive control in empirical tests.
10. Publish the configuration, primer file, reference-database metadata, final ASV table and raw-read manifest.
11. Interpret non-detections cautiously: they do not by themselves demonstrate species absence or primer failure.

### What the scripts do and do not automate

The numbered scripts preserve the main command sequence, but some transitions depend on manually curated Geneious files. File names such as `batra_primer_regions410aligned.fasta` and `batra_uniqueseq_itamph_alignment.fasta` refer to these manual outputs. For another primer, rename the files consistently or modify the script arguments.

Before running the first script from a separate analysis directory, provide its expected one-name-per-line input:

```bash
cp /path/to/this/repository/data/species_list_53.txt lista_anfibi.txt
bash /path/to/this/repository/Scripts/01_ncbi_download.sh
```

Subsequent scripts expect the output names documented in their source. Review each script before execution and keep a copy of the exact commands and software versions used for the new marker.

## Known limitations

- NCBI retrieval covered assembled Nucleotide records, not raw SRA reads.
- The list of 415 post-CRABS accessions was not available for release; this stage remains unresolved at accession level in `accession_flow.tsv`.
- Several steps depend on manual Geneious inspection and curated FASTA alignments that cannot be regenerated from accession lists alone.
- No comparative 16S analysis or degenerate-primer redesign was performed.
- The targeted revision searches did not recover a suitable Batra-region reference for *H. perrini* or an unambiguously attributable reference for *I. apuana*.
- The empirical public FASTA contains the amphibian component only and should not be used as a complete vertebrate database.
- The field dataset has limited spatial and temporal coverage. Non-detection in these samples should not be interpreted as evidence of species absence or primer failure.

## Software

| Tool | Role |
| --- | --- |
| NCBI Entrez Direct | Nucleotide queries and FASTA retrieval |
| CRABS | In silico PCR and taxonomic metadata assignment |
| Geneious Prime 2026.0.2 | Manual inspection and curation for the mismatch assessment |
| MAFFT | Sequence alignment |
| VSEARCH | Dereplication and sequence assignment |
| Python 3 with Biopython | FASTA header handling during per-species dereplication |
| R with PrimerMiner and Biostrings | Primer mismatch scoring |
| Barque v1.8.5 | Empirical read processing and ASV workflow |
| microDecon | Negative-control-based decontamination |

## Citation

When using the study data, cite the associated manuscript after publication. Until then, cite this repository together with the principal software and methodological references relevant to the reused components.

- Elbrecht V, Leese F (2017). PrimerMiner: an R package for development and in silico validation of DNA metabarcoding primers. *Methods in Ecology and Evolution* 8:622–626. <https://doi.org/10.1111/2041-210X.12687>
- Jeunen GJ et al. (2023). CRABS: a software program to generate curated reference databases for metabarcoding sequencing data. *Molecular Ecology Resources* 23:725–738. <https://doi.org/10.1111/1755-0998.13741>
- McKnight DT et al. (2019). microDecon: a highly accurate read-subtraction tool for the post-sequencing removal of contamination in metabarcoding studies. *Environmental DNA* 1:14–25. <https://doi.org/10.1002/edn3.11>
- Rognes T et al. (2016). VSEARCH: a versatile open source tool for metagenomics. *PeerJ* 4:e2584. <https://doi.org/10.7717/peerj.2584>
- Valentini A et al. (2016). Next-generation monitoring of aquatic biodiversity using environmental DNA metabarcoding. *Molecular Ecology* 25:929–942. <https://doi.org/10.1111/mec.13428>

## License and third-party data

Repository code is released under the [MIT License](LICENSE). Public database accessions remain subject to the attribution and reuse conditions of their source databases. The license does not transfer ownership of third-party NCBI or BOLD records.
