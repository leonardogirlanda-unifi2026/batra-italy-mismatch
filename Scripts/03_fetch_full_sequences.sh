grep "^>" batra_12S_amplicons.fasta | sed 's/^>//' > batra_amplicons_accessions.txt | efetch -db nuccore -format fasta -id "$(paste -sd, batra_amplicons_accessions.txt)" \
  > batra_full_sequences.fasta
