#Taxonomy database download
crabs db_download -s taxonomy

#Taxonomy assignment
crabs assign_tax \
  -i batra_primer_regions410aligned.fasta \
  -o batra_taxonomy.tsv \
  -a nucl_gb.accession2taxid \
  -t nodes.dmp \
  -n names.dmp \
  -w yes

#Count sequences per species (species in column 9 of taxonomy output):
cut -f9 batra_taxonomy.tsv | tail -n +2 | sort | uniq -c | sort -nr
