# CORBA: Contagious Recursive Blocking Attacks on Multi-Agent Systems Based on Large Language Models

## Citation

- Authors: Zhenhong Zhou, Zherui Li, Jie Zhang, Yuanhe Zhang, Kun Wang, Yang Liu, Qing Guo
- Year: 2026
- Venue: Findings of ACL 2026
- DOI: 10.18653/v1/2026.findings-acl.342
- Primary URL: https://aclanthology.org/2026.findings-acl.342/
- Open access URL: https://aclanthology.org/2026.findings-acl.342.pdf
- BibTeX key: `zhou2026corba`

## Paper Type

Attack; Evaluation; Empirical study

## Scope

### System Studied

LLM multi-agent systems with open-ended collaboration over varied communication
topologies.

### Multi-Agent Dependency

Recursive instructions force agents to trigger further messages, transforming
the collaboration graph into a resource-consuming cycle.

### Application Domain

General-purpose collaborative LLM systems.

## Security Model

- Protected assets: availability, bounded cost, and useful collaboration.
- Threat actor: source of a semantically benign recursive instruction.
- Trusted components: conventional model safety alignment.
- Attacker capabilities: introduce content that agents accept and recursively
  propagate.
- Security assumptions: agents can initiate messages or tasks for peers.

## Main Contribution

The paper formalizes Denial-of-Collaboration and introduces CORBA, a contagious
recursive blocking attack that induces meaningless communication cycles and
system paralysis.

## Attack or Failure

- Attack surface: open-ended inter-agent communication.
- Attack mechanism: benign-looking recursively contagious instructions.
- System-level failure: availability and resource-isolation failure.
- Security consequence: excessive resource use and system paralysis.

## Defense

- Defense mechanism: conventional safety alignment is evaluated, not introduced.
- Intervention point: content-level agent guardrails.
- Required observability: local semantic content in tested safeguards.
- Assumptions: semantically benign content is allowed.
- Limitations: baseline safeguards are not collaboration-aware.

## Evaluation

- Evaluated systems: multiple LLMs and communication topologies.
- Agent configuration: interacting agents capable of recursive communication.
- Dataset or environment: DoC attack tasks defined in the paper.
- Baselines: existing attacks and conventional safety alignment.
- Metrics: resource use, blocking, and paralysis outcomes.
- Main results: CORBA produces system paralysis in settings where baselines fail.

## Relation to Existing Work

- Claimed research gap: DoS targets nodes/services, while collaboration itself can
  be corrupted into self-sabotage.
- Closest related work: denial of service, prompt infection, and recursive agents.
- Difference from prior work: the attack payload can remain semantically benign.

## Relevance to Our SoK

- Included concepts: denial of collaboration, recursive delegation, contagious
  instructions, resource exhaustion.
- Taxonomy implications: availability is the violated property; recursion and
  contagion are mechanisms.
- Supported research questions: why content guardrails fail on systemic behavior.
- Important limitations: resource denominators differ from harmful-output ASR.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| DoC corrupts collaboration into self-sabotage and system paralysis. | Explicit author claim | Paper | Abstract; threat model | PDF 1 onward | Not applicable | Official abstract defines DoC. |
| CORBA uses benign recursively contagious instructions. | Explicit author claim | Paper | Abstract; method | PDF 1 onward | Not applicable | Official abstract describes the mechanism. |
| Conventional safety alignment is bypassed because content is semantically benign. | Explicit author claim | Paper | Abstract; experiments | PDF 1; evaluation | Not applicable | Reported in official abstract. |

## Provenance

- Discovery source: ACL Anthology; prior systematic search
- Discovery query: exact-title search
- Accessed version: published Findings of ACL 2026 version
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

