#!/usr/bin/env python3
"""Build reviewer-facing audit tables from the repository's existing lists.

The script deliberately leaves the original lists unchanged. It creates:

* results/species_screening_summary.tsv
* results/accession_flow.tsv
* results/review_audit_report.txt

If data/accessions_after_crabs_415.txt is added later, accession-level stages
will be resolved automatically without changing this script.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


SPECIES_SOURCES = {
    "evaluated": Path("data/evaluated_species_34.txt"),
    "no_sequences_retrieved": Path(
        "results/insilico_filtering_results/species_missing_no_sequences.txt"
    ),
    "no_batra_amplicon": Path(
        "results/insilico_filtering_results/species_no_batra_amplicon.txt"
    ),
    "incomplete_primer_binding_sites": Path(
        "results/insilico_filtering_results/species_incomplete_primer_sites.txt"
    ),
    "pending_sequence_audit": Path(
        "results/insilico_filtering_results/species_pending_sequence_audit.txt"
    ),
}


def read_lines(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def read_overrides(path: Path) -> dict[str, tuple[str, str]]:
    overrides: dict[str, tuple[str, str]] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            overrides[row["query_name"]] = (row["accepted_name"], row["note"])
    return overrides


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_species_summary(root: Path) -> tuple[list[dict[str, object]], list[str]]:
    target_path = root / "data/species_list_55.txt"
    override_path = root / "data/taxon_name_overrides.tsv"
    targets = read_lines(target_path)
    overrides = read_overrides(override_path)

    def canonical(name: str) -> str:
        return overrides.get(name, (name, ""))[0]

    outcome_by_taxon: dict[str, tuple[str, str]] = {}
    errors: list[str] = []

    for outcome, relative_path in SPECIES_SOURCES.items():
        for listed_name in read_lines(root / relative_path):
            accepted_name = canonical(listed_name)
            if accepted_name in outcome_by_taxon:
                previous = outcome_by_taxon[accepted_name]
                errors.append(
                    f"Species {accepted_name!r} occurs in both {previous[0]!r} and {outcome!r}."
                )
            outcome_by_taxon[accepted_name] = (outcome, relative_path.as_posix())

    rows: list[dict[str, object]] = []
    target_accepted_names: set[str] = set()
    for query_name in targets:
        accepted_name, note = overrides.get(query_name, (query_name, ""))
        target_accepted_names.add(accepted_name)
        match = outcome_by_taxon.get(accepted_name)
        if match is None:
            errors.append(f"Target species {query_name!r} has no screening outcome.")
            outcome, source_file = "unresolved", ""
        else:
            outcome, source_file = match
        rows.append(
            {
                "query_name": query_name,
                "accepted_name": accepted_name,
                "screening_outcome": outcome,
                "source_file": source_file,
                "note": note,
            }
        )

    for extra in sorted(set(outcome_by_taxon) - target_accepted_names):
        errors.append(f"Screening outcome exists for non-target or unmatched taxon {extra!r}.")

    return rows, errors


def build_accession_flow(root: Path) -> tuple[list[dict[str, object]], list[str], dict[str, int]]:
    initial = read_lines(root / "data/accessions_initial_919.txt")
    final = set(read_lines(root / "data/accessions_final_408.txt"))
    discarded = set(
        read_lines(root / "results/insilico_filtering_results/accessions_discarded_seq.txt")
    )
    intermediate_path = root / "data/accessions_after_crabs_415.txt"
    passed_crabs = set(read_lines(intermediate_path)) if intermediate_path.exists() else None

    initial_counts = Counter(initial)
    initial_unique = set(initial_counts)
    errors: list[str] = []

    if not final <= initial_unique:
        errors.append(f"{len(final - initial_unique)} final accessions are absent from the initial list.")
    if not discarded <= initial_unique:
        errors.append(f"{len(discarded - initial_unique)} discarded accessions are absent from the initial list.")
    if final & discarded:
        errors.append(f"{len(final & discarded)} accessions are both retained and manually discarded.")
    if passed_crabs is not None:
        if not passed_crabs <= initial_unique:
            errors.append(
                f"{len(passed_crabs - initial_unique)} CRABS accessions are absent from the initial list."
            )
        if not final <= passed_crabs:
            errors.append(f"{len(final - passed_crabs)} final accessions are absent from the CRABS list.")

    rows: list[dict[str, object]] = []
    for accession in sorted(initial_unique):
        retained = accession in final
        manual = accession in discarded
        if passed_crabs is None:
            passed_value: object = ""
            if retained:
                status = "retained_final_dataset"
            elif manual:
                status = "manually_discarded_after_crabs"
            else:
                status = "not_retained_stage_unresolved_without_415_list"
        else:
            passed_value = int(accession in passed_crabs)
            if retained:
                status = "retained_final_dataset"
            elif manual:
                status = "manually_discarded_after_crabs"
            elif accession in passed_crabs:
                status = "removed_during_manual_curation_or_incomplete_primer_sites"
            else:
                status = "not_recovered_by_crabs"

        rows.append(
            {
                "accession": accession,
                "initial_occurrences": initial_counts[accession],
                "passed_crabs": passed_value,
                "final_retained": int(retained),
                "manually_discarded": int(manual),
                "current_status": status,
            }
        )

    counts = {
        "initial_occurrences": len(initial),
        "initial_unique_accessions": len(initial_unique),
        "duplicated_initial_occurrences": len(initial) - len(initial_unique),
        "passed_crabs_unique_accessions": len(passed_crabs) if passed_crabs is not None else -1,
        "final_unique_accessions": len(final),
        "manually_discarded_accessions": len(discarded),
    }
    return rows, errors, counts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root (default: inferred from script location).",
    )
    args = parser.parse_args()
    root = args.repo_root.resolve()

    species_rows, species_errors = build_species_summary(root)
    accession_rows, accession_errors, counts = build_accession_flow(root)

    write_tsv(
        root / "results/species_screening_summary.tsv",
        ["query_name", "accepted_name", "screening_outcome", "source_file", "note"],
        species_rows,
    )
    write_tsv(
        root / "results/accession_flow.tsv",
        [
            "accession",
            "initial_occurrences",
            "passed_crabs",
            "final_retained",
            "manually_discarded",
            "current_status",
        ],
        accession_rows,
    )

    outcome_counts = Counter(row["screening_outcome"] for row in species_rows)
    report_lines = [
        "Reviewer-resource audit report",
        "==============================",
        "",
        f"Target taxa: {len(species_rows)}",
    ]
    report_lines.extend(
        f"  {outcome}: {count}" for outcome, count in sorted(outcome_counts.items())
    )
    report_lines.extend(
        [
            "",
            f"Initial accession occurrences: {counts['initial_occurrences']}",
            f"Unique initial accessions: {counts['initial_unique_accessions']}",
            f"Duplicate initial occurrences: {counts['duplicated_initial_occurrences']}",
            (
                "Unique accessions after CRABS: not available "
                "(add data/accessions_after_crabs_415.txt to resolve this stage)"
                if counts["passed_crabs_unique_accessions"] < 0
                else f"Unique accessions after CRABS: {counts['passed_crabs_unique_accessions']}"
            ),
            f"Unique final accessions: {counts['final_unique_accessions']}",
            f"Manually discarded accessions: {counts['manually_discarded_accessions']}",
            "",
        ]
    )
    errors = species_errors + accession_errors
    if errors:
        report_lines.append("ERRORS")
        report_lines.extend(f"- {error}" for error in errors)
    else:
        report_lines.append("Automated consistency checks: PASS")
    (root / "results/review_audit_report.txt").write_text(
        "\n".join(report_lines) + "\n", encoding="utf-8"
    )

    print("\n".join(report_lines))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
