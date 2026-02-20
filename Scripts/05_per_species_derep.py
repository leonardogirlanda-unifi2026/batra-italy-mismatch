#From taxonomy file created file with accession number and species
awk -F'\t' 'NR>1 {print $1 "\t" $9}' batra_taxonomy.tsv > acc_species.tsv

#Used acc_species.tsv to rename header of the unaligned sequences file (vsearch does not work with aligned fasta) 
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

#sequences divided in per-species fasta files
mkdir -p per_species

awk '
  /^>/ {
    split(substr($0,2), a, "|");
    sp=a[1];
    file="per_species/" sp ".fasta"
  }
  {print >> file}
' batra_amplicon_with_species.fasta


#dedup using vsearch  --derep_fulllength.
mkdir -p per_species_derep

for f in per_species/*.fasta; do
  sp=$(basename "$f" .fasta)
  vsearch --derep_fulllength "$f" \
          --output "per_species_derep/${sp}.derep.fasta" \
          --sizeout
done

#dedup sequences saved in per-species fasta files with each variant shown once and numerosity in the header
