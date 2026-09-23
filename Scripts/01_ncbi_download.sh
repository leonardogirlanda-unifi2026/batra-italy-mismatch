#!/usr/bin/env bash
set -euo pipefail

species_file="${1:-data/species_list_50.txt}"
overrides_file="${2:-data/taxon_name_overrides.tsv}"
output_file="${3:-italian_amphibians_12S.fasta}"

: > "$output_file"

while IFS= read -r species; do
  [[ -z "$species" ]] && continue

  query_names=("$species")
  while IFS=$'\t' read -r query_name accepted_name note; do
    [[ "$query_name" == "query_name" ]] && continue
    if [[ "$species" == "$query_name" || "$species" == "$accepted_name" ]]; then
      [[ " ${query_names[*]} " == *" $query_name "* ]] || query_names+=("$query_name")
      [[ " ${query_names[*]} " == *" $accepted_name "* ]] || query_names+=("$accepted_name")
    fi
  done < "$overrides_file"

  organism_query=""
  for name in "${query_names[@]}"; do
    [[ -n "$organism_query" ]] && organism_query+=" OR "
    organism_query+="\"$name\"[Organism]"
  done

  query="($organism_query) AND mitochondrion[filter] AND (\"50\"[SLEN] : \"30000\"[SLEN]) AND (12S[All Fields] OR \"12S ribosomal RNA\"[All Fields] OR \"small subunit ribosomal RNA\"[All Fields] OR \"mitochondrial small subunit ribosomal RNA\"[All Fields] OR (\"5000\"[SLEN] : \"30000\"[SLEN]))"

  echo "### $species" >&2
  echo ">#SPECIES $species" >> "$output_file"
  esearch -db nuccore -query "$query" </dev/null \
    | efetch -format fasta >> "$output_file"

  sleep 0.34
done < "$species_file"
