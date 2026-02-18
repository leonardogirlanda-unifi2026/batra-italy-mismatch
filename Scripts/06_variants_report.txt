#creates a tsv with number of sequences. number of variants and numerosity of the most common variant per species
echo -e "species\tn_sequences\tn_variants\tmax_variant_count" > haplotype_report.tsv

for f in per_species_derep/*.derep.fasta; do
  sp=$(basename "$f" .derep.fasta)

  n_seq=$(grep -o "size=[0-9]*" "$f" | sed 's/size=//' | awk '{s+=$1} END{print s}')
  n_var=$(grep -c "^>" "$f")
  max_var=$(grep -o "size=[0-9]*" "$f" | sed 's/size=//' | sort -nr | head -n 1)

  echo -e "${sp}\t${n_seq}\t${n_var}\t${max_var}" >> haplotype_report.tsv
done

