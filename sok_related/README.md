# Strongly Related Multi Agent Security SoKs

This directory is a **supporting comparator view** for related SoKs, surveys, and framework papers. It is not an active corpus partition.

The only manuscript corpus denominator in this repository is **201 works**, defined by `corpus/set1_core.csv` and `corpus/set2_emerging.csv`.

## Purpose

The files here help compare the manuscript with especially close multi agent security and agentic security systematizations. Some comparator records may also be members of the final 201 corpus. Others may be broader contextual works. Because overlap is allowed, the number of rows in this directory must never be added to 201.

## Files

* `papers.csv` contains the supporting comparator records.
* `references.bib` contains citations for those records.
* `exclusions.csv` records comparator specific screening decisions when needed.

When a comparator is also in the final corpus, use its canonical note under `papers/` for corpus membership and technical evidence. Use this directory only for the comparative related work view.

## Rules

1. Never treat `sok_related/` as Set 1, Set 2, or an additional paper set.
2. Never use its row count to change the 201 manuscript denominator.
3. Prefer the published version of a comparator when available.
4. Keep direct MAS centered surveys distinct from broader agent security comparators through the existing relation fields.
5. Use primary papers rather than survey summaries for empirical attack, defense, or prevalence claims whenever possible.
