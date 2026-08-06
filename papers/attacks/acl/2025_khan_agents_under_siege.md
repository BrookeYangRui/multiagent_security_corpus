# Agents Under Siege: Breaking Pragmatic Multi-Agent LLM Systems with Optimized Prompt Attacks

## Citation

- Authors: Rana Shahroz, Zhen Tan, Sukwon Yun, Charles Fleming, Tianlong Chen
- Year: 2025
- Venue: ACL 2025
- DOI: 10.18653/v1/2025.acl-long.476
- Primary URL: https://aclanthology.org/2025.acl-long.476/
- Open access URL: https://aclanthology.org/2025.acl-long.476.pdf
- BibTeX key: `khan2025agentsundersiege`

## Paper Type

Attack; Evaluation; Empirical study

## Scope

### System Studied

Pragmatic multi-agent LLM systems with communication latency, limited token
bandwidth, varied graph topology, and distributed safety mechanisms.

### Multi-Agent Dependency

The attack optimizes how adversarial prompt components traverse a constrained
agent network; message ordering, routes, and distributed defenses are part of
the attack objective.

### Application Domain

General-purpose multi-agent workflows.

## Security Model

- Protected assets: integrity and safety of the collective system output.
- Threat actor: an adversary able to introduce optimized prompt content into the
  network.
- Trusted components: nominally honest agents and distributed safeguards.
- Attacker capabilities: optimize prompt distribution over network paths while
  accounting for latency and bandwidth.
- Security assumptions: agents exchange messages and make decentralized
  reasoning decisions.

## Main Contribution

The paper introduces a permutation-invariant prompt attack formulated with
graph-based maximum-flow/minimum-cost optimization and a Permutation-Invariant
Evasion Loss for constrained multi-agent networks.

## Attack or Failure

- Attack surface: messages, graph paths, and distributed safety checks.
- Attack mechanism: distribute optimized adversarial prompt components across
  communication paths to evade detection.
- System-level failure: collective decision and safety-integrity failure.
- Security consequence: unsafe output despite distributed safeguards.

## Defense

- Defense mechanism: Llama-Guard and PromptGuard variants are evaluated, not
  introduced.
- Intervention point: agent/message content filters.
- Required observability: local content presented to each guard.
- Assumptions: safeguards inspect distributed prompt fragments locally.
- Limitations: evaluated defenses do not reliably prohibit the attack.

## Evaluation

- Evaluated systems: Llama, Mistral, Gemma, DeepSeek, and other model variants in
  multi-agent configurations.
- Agent configuration: multiple constrained network topologies.
- Dataset or environment: JailbreakBench and AdversarialBench among the reported
  datasets.
- Baselines: conventional attacks and guard variants.
- Metrics: attack success and detection/evasion outcomes.
- Main results: the authors report improvements up to 7x over conventional
  attacks in the evaluated settings.

## Relation to Existing Work

- Claimed research gap: prior attacks do not represent latency, bandwidth, and
  distributed defenses in pragmatic multi-agent systems.
- Closest related work: prompt injection, jailbreak optimization, and infectious
  attacks.
- Difference from prior work: optimizes prompt distribution over the system
  graph rather than attacking one prompt in isolation.

## Relevance to Our SoK

- Included concepts: topology-aware optimization, bandwidth, latency,
  distributed guard evasion.
- Taxonomy implications: topology is a precondition/amplifier, not the violated
  security property itself.
- Supported research questions: whether distributed guardrails compose under
  fragmented attacks.
- Important limitations: evaluation scope does not establish behavior for every
  deployed framework or closed model.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The attack accounts for latency, token bandwidth, topology, and defenses. | Explicit author claim | Paper | Abstract; Introduction | PDF 1-2 | Not applicable | The official abstract defines the pragmatic constraints. |
| The method uses maximum-flow/minimum-cost optimization and PIEL. | Explicit author claim | Paper | Abstract; method | PDF 1; method section | Not applicable | Named in the official abstract. |
| Existing Llama-Guard and PromptGuard variants fail to prohibit the attack in the evaluation. | Explicit author claim | Paper | Abstract; experiments | PDF 1; results | Not applicable | Reported in the official abstract. |

## Provenance

- Discovery source: prior corpus; ACL Anthology
- Discovery query: exact-title search
- Accessed version: published ACL 2025 version
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

