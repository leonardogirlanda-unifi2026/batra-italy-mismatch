#!/usr/bin/env bash
set -euo pipefail

# Create a two-column accession/species file from the CRABS taxonomy output.
awk -F'\t' 'NR>1 {print $1 "\t" $9}' batra_taxonomy.tsv > acc_species.tsv

# Use acc_species.tsv to rename the unaligned FASTA headers. VSEARCH
# dereplication is performed on unaligned sequences.
python3 - <<'PY'
from Bio import SeqIO

acc2sp = {}
with open("acc_species.tsv") as f:
    for line in f:
        acc, sp = line.rstrip().split("\t")
        acc2sp[acc] = sp.replace(" ", "_")

with open("batra_amplicon_with_species.fasta", "w") as out:
    for rec in SeqIO.parse("batra_primer_regions410unaligned.fasta", "fasta"):
        acc = rec.id.split("|")[0]
        sp = acc2sp.get(acc, "UNKNOWN")
        rec.id = f"{sp}|{acc}"
        rec.description = ""
        SeqIO.write(rec, out, "fasta")
PY

# Divide sequences into per-species FASTA files.
mkdir -p per_species

awk '
  /^>/ {
    split(substr($0,2), a, "|");
    sp=a[1];
    file="per_species/" sp ".fasta"
  }
  {print >> file}
' batra_amplicon_with_species.fasta


# Dereplicate full-length sequences within each species.
mkdir -p per_species_derep

for f in per_species/*.fasta; do
  sp=$(basename "$f" .fasta)
  vsearch --derep_fulllength "$f" \
          --output "per_species_derep/${sp}.derep.fasta" \
          --sizeout
done

# Each output contains one record per sequence variant and its abundance in the header.
