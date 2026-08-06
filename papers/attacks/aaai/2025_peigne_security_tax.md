# Multi-Agent Security Tax: Trading Off Security and Collaboration Capabilities in Multi-Agent Systems

## Citation

- Authors: Pierre Peigne, Mikolaj Kniejski, Filip Sondej, Matthieu David, Jason Hoelscher-Obermaier, Christian Schroeder de Witt, Esben Kran
- Year: 2025
- Venue: AAAI 2025
- DOI: 10.1609/aaai.v39i26.34970
- Primary URL: https://ojs.aaai.org/index.php/AAAI/article/view/34970
- Open access URL: https://ojs.aaai.org/index.php/AAAI/article/download/34970/37125
- BibTeX key: `peigne2025securitytax`

## Paper Type

Attack; Defense; Evaluation; Empirical study

## Scope

### System Studied

Communicating LLM agents collaborating in an autonomous chemical-research
facility simulation.

### Multi-Agent Dependency

One compromised member disseminates malicious instructions across multiple hops;
the measured trade-off is between system-wide robustness and collaboration.

### Application Domain

Autonomous scientific collaboration.

## Security Model

- Protected assets: collective objective integrity and safe collaboration.
- Threat actor: attacker controlling one agent.
- Trusted components: initially benign peers and tested defense prompts/memories.
- Attacker capabilities: inject a malicious prompt that peers may forward.
- Security assumptions: natural-language communication influences peer behavior.

## Main Contribution

The paper demonstrates infectious malicious prompts and evaluates four mitigation
strategies, showing a security-collaboration trade-off in the studied network.

## Attack or Failure

- Attack surface: messages and agent memories.
- Attack mechanism: multi-hop malicious-instruction propagation.
- System-level failure: propagation and collective-objective integrity failure.
- Security consequence: system-wide fulfillment of misaligned instructions.

## Defense

- Defense mechanism: two memory-vaccination and two generic safety-instruction
  strategies.
- Intervention point: agent memory and instruction context.
- Required observability: local malicious input; no global monitor is required by
  all tested variants.
- Assumptions: false memories and safety instructions influence later behavior.
- Limitations: defenses reduce normal collaboration in the reported experiments.

## Evaluation

- Evaluated systems: multiple underlying LLMs in one agent-network simulation.
- Agent configuration: one compromised agent and collaborating peers.
- Dataset or environment: autonomous chemical-research facility simulation.
- Baselines: undefended network and four defense variants.
- Metrics: spread/fulfillment of malicious instructions, robustness, cooperation.
- Main results: mitigations reduce attack spread but also reduce collaboration.

## Relation to Existing Work

- Claimed research gap: systemic security trade-offs in strongly interacting LLM
  agent networks remain poorly understood.
- Closest related work: prompt injection, computer worms, and multi-agent
  collaboration.
- Difference from prior work: jointly measures attack containment and benign
  collaboration loss.

## Relevance to Our SoK

- Included concepts: compromised member, infection, vaccination, security-utility
  trade-off.
- Taxonomy implications: defense cost belongs in the measurement contract rather
  than the failure taxonomy.
- Supported research questions: whether local defenses preserve system utility.
- Important limitations: one simulated application and selected models.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| One compromised agent spreads malicious instructions over multiple hops. | Explicit author claim | Paper | Abstract; Introduction | PDF 1 | Not applicable | Official AAAI paper describes infectious prompts. |
| Four defense strategies are evaluated. | Explicit author claim | Paper | Abstract; contributions | PDF 1 | Not applicable | Two vaccination and two safety-instruction variants are named. |
| Defenses reduce spread and collaboration capability. | Explicit author claim | Paper | Abstract; experiments | PDF 1; results | Not applicable | Reported security-collaboration trade-off. |

## Provenance

- Discovery source: prior corpus; AAAI proceedings
- Discovery query: exact-title search
- Accessed version: published AAAI 2025 version
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

