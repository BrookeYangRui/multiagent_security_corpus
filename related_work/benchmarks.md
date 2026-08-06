# Benchmarks

Cross-paper synthesis of evaluation settings, baselines, metrics, denominators,
and verification methods.

## Corpus Map

**Established finding.** The evaluation-primary corpus contains 21 canonical
records: 12 formal conference, journal, or workshop versions and 9 arXiv-only
versions. The formal records are organized under `papers/evaluations/`; the
arXiv records are isolated under `papers/evaluations/arxiv/`.

**Cross-paper observation.** Evaluation units vary across task, instance,
agent, message, sensitive item, trace, game, and population. TAMAS and ACIARena
use attack/task cases; AgentLeak uses channels and sensitive items; Colosseum
separates conversation evidence from action regret; HARP uses paired traces;
CalBench combines agent-level privacy with group-level utility. These measures
must not share a denominator without an explicit conversion contract. See
`corpus/evaluation_artifacts.csv` and the notes keyed by
`kavathekar2026tamas`, `elyagoubi2026agentleak`, `nakamura2026colosseum`,
`rahman2026harp`, and `zou2026calbench`.

**Established finding.** Several evaluation-primary works require global
observability: AgentLeak instruments internal channels, GAMMAF uses attributed
communication graphs, HARP reads the full trace, and MAC-Bench audits procedural
execution rather than only the final response. This supports the SoK's defense
contract distinction between local output checks and system-level properties.

**Author-claimed gap.** TAMAS and ACIARena argue that single-agent benchmarks
miss interaction-dependent attacks. A2ASecBench makes the agent-to-agent
protocol boundary executable, MedSentry compares insider attacks across four
topologies, and PEAR isolates planner versus executor attack position. These
are claims made by the respective papers, not a new prevalence estimate.

**Our interpretation.** The corpus is best read as three linked layers:
benchmark construction, attack/defense evaluation, and measurement contract.
Artifact rows for attack-primary papers remain in
`corpus/evaluation_artifacts.csv`; their canonical notes are not duplicated in
`papers/evaluations/`.

## Canonical Evaluation Notes

| Venue | BibTeX keys |
| --- | --- |
| ACL / ACL Demo | `kavathekar2026tamas`, `an2026aciarena`, `gonzalez2026multimodalsafety`, `jiang2026risklab` |
| AAAI / AAMAS / COLM | `olson2026liecraft`, `milkowski2026amongus`, `arora2026safeagents`, `nother2026badacts` |
| ICLR / Findings EACL | `dong2026pear`, `li2026a2asecbench` |
| IEEE Access / NeurIPS workshop | `elyagoubi2026agentleak`, `juneja2025magpie` |
| arXiv | `chen2025medsentry`, `jia2026masfire`, `lemercier2026gambit`, `mateotorrejon2026gammaf`, `rahman2026harp`, `zou2026calbench`, `nakamura2026colosseum`, `zhao2026macbench` |

Defense-primary evaluation protocols, including `miao2026blindguard`, remain
under `papers/defenses/` and are linked only through the artifact index.

## Artifact Index Rule

`corpus/evaluation_artifacts.csv` is the single index for reusable datasets,
harnesses, and metrics. Each row has one `canonical_paper_id`, one note path,
the measurement unit, denominator, metrics, availability URL, and publication
status. An attack- or defense-primary paper is never copied into the evaluation
directory merely because it contains an evaluation artifact.
