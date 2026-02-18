#PrimerMiner richiede un FASTA allineato con posizioni primer coerenti (qui: forward 1–17; reverse 76–98).

library(PrimerMiner)
library(Biostrings)

evaluate_primer(
  "batra_uniqueseq_itamph_alignment.fasta",
  "ACACCGCCCGTCACCCT",
  1, 17,
  save = "Batra_F_eval.csv",
  mm_position = "Position_v1",
  adjacent = 2,
  mm_type = "Type_v1"
)

evaluate_primer(
  "batra_uniqueseq_itamph_alignment.fasta",
  "GTAYACTTACCATGTTACGACTT",
  76, 98,
  save = "Batra_R_eval.csv",
  mm_position = "Position_v1",
  adjacent = 2,
  mm_type = "Type_v1",
  forward = FALSE
)
