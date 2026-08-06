# From Shield to Target: Denial-of-Service Attacks on LLM-Based Agent Guardrails

## Citation

- Authors: Yuguang Zhou, Xunguang Wang, Pingchuan Ma, Zhantong Xue, Zhaoyu Wang, Shuai Wang
- Year: 2026
- Venue: arXiv
- DOI: 10.48550/arXiv.2606.14517
- Primary URL: https://arxiv.org/abs/2606.14517
- Open access URL: https://arxiv.org/pdf/2606.14517
- BibTeX key: `zhou2026shieldtarget`

## Paper Type

Attack; Evaluation; Empirical study

Primary category: attack

Scope relation: security_relevant

## Scope

### System Studied

LLM-based runtime guardrails deployed for web, desktop, code, and multi-agent
systems, including co-located agents sharing guardrail infrastructure.

### Multi-Agent Dependency

The primitive targets a guardrail and also applies to single-agent systems. Its
MAS-specific consequence is head-of-line blocking and starvation of other agents
sharing the guardrail service, so the paper is security-relevant rather than a
purely MAS-native attack.

### Application Domain

Autonomous agent deployments with runtime safety monitors.

## Security Model

- Protected assets: guardrail availability, agent throughput, and safe execution.
- Threat actor: external source able to place content an agent will read.
- Trusted components: agent policy and guardrail implementation.
- Attacker capabilities: inject structured natural-language content only.
- Security assumptions: guardrail inference lies on the action-critical path.

## Main Contribution

The paper develops transferable payloads that induce extended guardrail
reasoning. It evaluates systemic effects when agents share the affected guardrail
infrastructure.

## Attack or Failure

- Attack surface: untrusted content passed to reasoning guardrails.
- Attack mechanism: schema-shaped payloads extend guardrail generation.
- System-level failure: shared-service availability and resource-isolation failure.
- Security consequence: latency amplification, blocked actions, and peer starvation.

## Defense

The paper evaluates filters and token/time budgets. It argues that fail-open and
fail-closed timeout handling trade safety bypass against denial of service.

## Evaluation

- Evaluated systems: standalone guardrails and web, desktop, code, and LangGraph
  multi-agent deployments.
- Agent configuration: co-located agents sharing guardrail infrastructure.
- Dataset or environment: representative agent benchmarks and poisoned content.
- Baselines: prior reasoning-extension and adversarial-input methods.
- Metrics: generated tokens, latency amplification, throughput, and task success.
- Main results: the paper reports cross-model transfer and MAS head-of-line
  blocking under its evaluated deployment.

## Relevance to Our SoK

- Included concepts: DoS, shared monitor bottleneck, resource isolation.
- Taxonomy implications: distinguish a general guardrail attack primitive from
  its interaction-amplified population consequence.
- Important limitations: arXiv-only; MAS is one of four deployment evaluations.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The attack injects content that prolongs guardrail reasoning. | Explicit author claim | Paper | Abstract; Sec. 3-5 | 1, 4-7 | Fig. 1 | Payloads mimic the guardrail's analytical schema. |
| Multi-agent evaluation uses transform-resilient payloads. | Explicit author claim | Paper | Sec. 1; 7.2 | 2, 11-12 | Table 10 | Intermediate rewriting is treated as the MAS-specific constraint. |
| A poisoned worker degrades co-located agents through shared guardrail service. | Explicit author claim | Paper | Sec. 7.2; conclusion | 12, 16 | Table 10 | The paper reports throughput loss and head-of-line blocking. |
| The primitive is not unique to MAS. | Corpus interpretation | Paper | Sec. 7 | 10-15 | Not applicable | The same attack is evaluated on web, desktop, and code agents. |

## Provenance

- Discovery source: systematic screening ledger; arXiv API
- Discovery query: denial of service multi-agent LLM
- Accessed version: arXiv v2
- Access date: 2026-08-06
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-06
