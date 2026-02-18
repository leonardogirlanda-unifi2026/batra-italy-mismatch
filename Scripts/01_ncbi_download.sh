# Output FASTA
: > italian_amphibians_12S.fasta

# reads species from FASTA file
mapfile -t species_list < lista_anfibi.txt

# Download NCBI seq fro each species
for species in "${species_list[@]}"; do
  [[ -z "$species" ]] && continue
  echo "### $species" >&2
  echo ">#SPECIES $species" >> italian_amphibians_12S.fasta

  esearch -db nuccore -query "\"$species\"[Organism] AND mitochondrion[filter] AND (12S[All Fields] OR \"12S ribosomal RNA\"[All Fields] OR \"small subunit ribosomal RNA\"[All Fields] OR \"mitochondrial small subunit ribosomal RNA\"[All Fields]) AND (\"50\"[SLEN] : \"30000\"[SLEN])" </dev/null \
  | efetch -format fasta >> italian_amphibians_12S.fasta

  sleep 0.2
done
