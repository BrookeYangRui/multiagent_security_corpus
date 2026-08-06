# Strongly Related Multi-Agent Security SoKs

This synthesis uses `sok_related/papers.csv`, not the canonical research corpus.
The two denominators must be reported separately.

## Direct Multi-Agent Security Agendas

- **Established finding:** `schroederdewitt2025openchallenges` defines
  multi-agent security around threats that emerge or amplify through agent
  interaction. Its arXiv v2 taxonomy covers collusion, exploitation, swarm and
  cascade attacks, conflict, embodied security, and sociotechnical threats; see
  `papers/surveys/arxiv/2025_schroeder_de_witt_open_challenges.md`.
- **Established finding:** `ko2026sevenchallenges` isolates seven security
  challenges in cross-domain multi-agent LLM systems without a common trust
  authority and pairs them with evaluation and mitigation directions; see
  `papers/surveys/journals_npj_ai/2026_ko_seven_challenges.md`.

## Strong Risk And Governance Comparators

- **Established finding:** `hammond2025multiagentrisks` organizes advanced
  multi-agent risk into miscoordination, conflict, and collusion plus seven
  cross-cutting factors. Multi-agent security is one factor inside this broader
  safety, governance, and ethics framework; see
  `papers/surveys/technical_reports/2025_hammond_multi_agent_risks.md`.
- **Established finding:** `raza2026trism` adapts trust, risk, security,
  privacy, ModelOps, explainability, and lifecycle governance to agentic
  multi-agent systems; see
  `papers/surveys/journals_ai_open/2026_raza_trism.md`.

## Cross-Paper Observation

- **Cross-paper observation:** The four works agree that isolated-agent safety
  does not establish system security once agents communicate, share state,
  coordinate, or cross trust domains. They differ in unit of analysis:
  interaction-dependent threats, cross-domain security challenges, broad
  multi-agent risks, and lifecycle governance.
- **Our interpretation:** None supplies an empirical prevalence denominator.
  Their taxonomies and agendas are comparison frames; primary attack, defense,
  and evaluation claims must still come from the 107-paper research corpus.

## Exclusion Boundary

- **Our interpretation:** General LLM-agent security surveys are excluded when
  multi-agent interaction is only one component or subsection. Decisions are
  recorded in `sok_related/exclusions.csv`; a mention of multi-agent attacks is
  not sufficient for this strongly related set.
