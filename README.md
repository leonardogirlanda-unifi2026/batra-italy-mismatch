# batra-italy-mismatchbatra-italy-mismatch/
├─ README.md
├─ CITATION.cff
├─ LICENSE
├─ data/
│  ├─ species_lists/
│  │  ├─ target_taxa_53.txt
│  │  ├─ evaluated_species_34.txt
│  │  └─ missing_taxa_19.txt
│  ├─ accessions/
│  │  ├─ ncbi_initial_972_accessions.txt
│  │  ├─ batra_amplicon_accessions_415.txt
│  │  └─ curated_outliers_removed.txt
│  └─ references/
│     ├─ batra_uniqueseq_variants.fasta
│     └─ batra_taxonomy.tsv
├─ results/
│  ├─ Table1_mismatch_summary.tsv
│  ├─ Batra_F_eval.csv
│  └─ Batra_R_eval.csv
├─ scripts/
│  ├─ 01_ncbi_download.sh
│  ├─ 02_crabs_insilico_pcr.sh
│  ├─ 03_fetch_full_sequences.sh
│  ├─ 04_trim_primer_regions.sh
│  ├─ 05_assign_tax.sh
│  ├─ 06_per_species_derep.sh
│  └─ 07_primerminer_eval.R
└─ docs/
   ├─ workflow.md
   ├─ database_curation.md
   └─ faq.md
