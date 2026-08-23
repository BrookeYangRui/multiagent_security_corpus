# Collaborative Shadows: Distributed Backdoor Attacks in LLM-Based Multi-Agent Systems

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set2_emerging` · `attack` · venue `arXiv` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation

- Authors: Pengyu Zhu, Lijun Li, Yaxing Lyu, Li Sun, Sen Su, Jing Shao
- Year: 2025
- Venue: arXiv preprint
- DOI: 10.48550/arXiv.2510.11246
- Primary URL: https://arxiv.org/abs/2510.11246
- Open access URL: https://arxiv.org/pdf/2510.11246
- BibTeX key: `zhu2025collaborativeshadows`

## Paper Type

Attack; Benchmark; Evaluation; Empirical study

## Scope

### System Studied

Tool-using, role-specialized MAS in which public and private tools are invoked in
a workflow sequence to solve database and multi-role collaboration tasks.

### Multi-Agent Dependency

The backdoor is split across tools owned or invoked by different agents; each
primitive is dormant alone and the payload assembles only under a designated
cross-agent collaboration sequence.

### Application Domain

Database operations and multi-role tool collaboration.

## Security Model

- Protected assets: confidential data, tool integrity, and authorized execution.
- Threat actor: a tool or supply-chain adversary that plants distributed
  primitives and controls a triggering instruction.
- Trusted components: base models and most tools remain benign.
- Attacker capabilities: poison selected tool implementations or descriptions and
  induce a specific tool-use sequence.
- Security assumptions: agents can invoke public and role-private tools whose
  outputs or side effects compose across the workflow.

## Main Contribution

The paper introduces a training-free distributed backdoor whose primitives are
individually inactive but assemble through agent collaboration. It also releases
a sandbox and a multi-role collaboration benchmark.

## Attack or Failure

- Attack surface: tool supply chain, role-private capabilities, public tools, and
  cross-agent invocation order.
- Attack mechanism: conditional primitives distributed among tools activate and
  assemble a final payload only after the trigger sequence.
- System-level failure: compositional authorization and confidentiality failure.
- Security consequence: targeted behavior such as data exfiltration with little
  effect on benign-task accuracy.

## Defense

- Defense mechanism: Not proposed as a complete defense.
- Intervention point: Not applicable.
- Required observability: detecting the full backdoor would require cross-tool,
  cross-agent provenance and sequence visibility.
- Assumptions: local tool inspection sees no independently active payload.
- Limitations: benchmark tool suites and attack primitives are constructed in a
  sandbox and do not establish prevalence in deployed systems.

## Evaluation

- Evaluated systems: a sandboxed MAS using several contemporary LLMs.
- Agent configuration: role-specific agents with public and private tool sets.
- Dataset or environment: AgentBench-MAS (DB), Multi-Role Collaboration Bench,
  and a MultiAgentBench subset.
- Baselines: clean tools, poisoned tools without the trigger, and ablations that
  remove attack components.
- Metrics: attack success rate, benign accuracy, and accidental trigger rate.
- Main results: ASR exceeds 98% on AgentBench-MAS (DB) and 95% on the Multi-Role
  benchmark for the main evaluated models, while benign accuracy is nearly
  unchanged.

## Relation to Existing Work

- Claimed research gap: single-agent backdoors do not model primitives that
  activate only through collaboration.
- Closest related work: tool poisoning, conjunctive prompt attacks, and LLM
  backdoors.
- Difference from prior work: no one tool or agent carries the complete active
  backdoor.

## Relevance to Our SoK

- Included concepts: distributed authority, private tools, invocation sequence,
  dormant primitives, provenance, and sandboxed execution.
- Taxonomy implications: primitive distribution and sequence are mechanisms and
  preconditions; unauthorized global action is the failure property.
- Supported research questions: whether local scanning composes into protection
  when authority and payload fragments are distributed.
- Important limitations: preprint status, synthetic tasks, and low baseline
  capability on the MultiAgentBench subset constrain external validity.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| Backdoor primitives are inactive alone and assemble under a collaboration sequence. | Explicit author claim | Paper | 3 | PDF 4-6 | Figure 2 | The attack construction distributes conditional and final primitives among tools. |
| Main evaluation uses two new MAS benchmark adaptations. | Explicit author claim | Paper | 4.2; Appendix B | PDF 7; 15-17 | Not applicable | AgentBench-MAS (DB) and Multi-Role Collaboration Bench are described in detail. |
| Main ASR exceeds 95% with little benign degradation. | Explicit author claim | Paper | 4.3 | PDF 7-9 | Table 1; Figures 3-4 | Results separate triggered attack success from clean and poison-only accuracy. |
| Detecting the complete mechanism requires sequence-wide provenance. | Interpretation | Paper | 3; 5.1 | PDF 4-6; 9 | Figure 5 | Individual primitives do not reveal the assembled cross-agent behavior. |

## Provenance

- Discovery source: arXiv; citation snowballing from conjunctive attacks
- Discovery query: `Collaborative Shadows distributed backdoor publication`
- Accessed version: arXiv v1
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05
