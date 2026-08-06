# FuncPoison: Poisoning Function Library to Hijack Multi-agent Autonomous Driving Systems

## Citation

- Authors: Yuzhen Long, Songze Li
- Year: 2025
- Venue: arXiv
- DOI: 10.48550/arXiv.2509.24408
- Primary URL: https://arxiv.org/abs/2509.24408
- Open access URL: https://arxiv.org/pdf/2509.24408
- BibTeX key: `long2025funcpoison`

## Paper Type

Attack; Evaluation; Empirical study

Primary category: attack

Scope relation: core_security

## Scope

### System Studied

LLM-based autonomous-driving pipelines with specialized perception, memory,
reasoning, and planning agents using a shared function library.

### Multi-Agent Dependency

A poisoned function first changes one agent's output and the corrupted result is
then consumed by downstream agents, producing a controllable cascade through the
decision pipeline.

### Application Domain

Autonomous driving.

## Security Model

- Protected assets: trajectory integrity and collision avoidance.
- Threat actor: malicious or compromised function-library provider.
- Trusted components: models, prompts, and normal inter-agent pipeline.
- Attacker capabilities: add deceptive function descriptions and callable tools.
- Security assumptions: agents trust and invoke shared library entries.

## Main Contribution

FuncPoison targets the shared function library rather than model weights or
ordinary prompts. It is evaluated on AgentDriver and AgentThink and supports
direct and downstream attack paths.

## Attack or Failure

- Attack surface: shared tool and function metadata.
- Attack mechanism: template-shaped malicious function descriptions.
- System-level failure: compositional action-integrity failure.
- Security consequence: trajectory deviation and increased collisions.

## Defense

The paper evaluates instruction constraints and filtering-oriented defenses; it
does not establish a complete preventive defense.

## Evaluation

- Evaluated systems: AgentDriver and AgentThink.
- Agent configuration: specialized driving agents connected as pipelines.
- Dataset or environment: nuScenes-derived autonomous-driving tasks.
- Baselines: GCG, AutoDAN, CPA, BadChain, and AgentPoison.
- Metrics: L2 trajectory error, collision rate, and thresholded ASR.
- Main results: the paper reports high ASR and downstream propagation under its
  evaluated settings.

## Relevance to Our SoK

- Included concepts: shared tool poisoning, authority cascade, propagation.
- Taxonomy implications: the initial function compromise is a mechanism; the
  downstream trajectory error is the system-level failure.
- Important limitations: arXiv-only and limited to two driving architectures.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| FuncPoison poisons a shared function library used by LLM driving agents. | Explicit author claim | Paper | Abstract; Sec. 1 | 1-2 | Fig. 1 | The attack inserts malicious tools with deceptive descriptions. |
| Corruption can propagate from a selected agent to downstream agents. | Explicit author claim | Paper | Sec. 1; method | 2, 4 | Fig. 2-3 | The paper distinguishes direct and indirect pipeline paths. |
| Evaluation uses AgentDriver and AgentThink. | Explicit author claim | Paper | Sec. 5 | 6-8 | Table 2; Fig. 5-6 | Both systems are evaluated against multiple baselines. |
| Reported ASR depends on an L2-error threshold. | Explicit author claim | Paper | Sec. 5 | 7 | Fig. 5-6 | Results provide ASR at L2 thresholds 3 and 6. |

## Provenance

- Discovery source: systematic screening ledger; arXiv API
- Discovery query: shared memory poisoning multi-agent LLM
- Accessed version: arXiv v2
- Access date: 2026-08-06
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-06
