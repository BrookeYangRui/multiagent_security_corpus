# MedSentry: Understanding and Mitigating Safety Risks in Medical LLM Multi-Agent Systems

## Citation

Title: MedSentry: Understanding and Mitigating Safety Risks in Medical LLM Multi-Agent Systems

Authors: Kai Chen; Taihang Zhen; Hewei Wang; Kailai Liu; Xinfeng Li; Jing Huo; Tianpei Yang; Jinfeng Xu; Wei Dong; Yang Gao

Year: 2025

Venue: arXiv

DOI: 10.48550/arXiv.2505.20824

Primary URL: https://arxiv.org/abs/2505.20824

Open access URL: https://arxiv.org/pdf/2505.20824

BibTeX key: chen2025medsentry

## Paper Type

Benchmark; Evaluation; Attack; Defense; Empirical study

## Scope

### System Studied

Five-agent medical collaborations instantiated as layered, shared-pool, centralized, and decentralized topologies.

### Multi-Agent Dependency

One insider agent introduces harmful medical content whose influence and containment depend on information routing, aggregation, redundancy, and isolation across the four topologies.

### Application Domain

Medical question answering and safety-critical clinical guidance.

## Security Model

### Protected Assets

Safety and reliability of the collective medical response.

### Threat Actor

A compromised insider agent prompted with a dark-personality role and a harmful medical request.

### Trusted Components

The evaluation harness, benchmark labels, evaluator agent, and optional enforcement agent.

### Attacker Capabilities

The malicious member participates through the topology's ordinary communication channels and can conceal intent in its utterances.

### Security Assumptions

Agent count and backbone are controlled for topology comparisons; an evaluator can score the system response against safety principles.

## Main Contribution

MedSentry contributes 5,000 adversarial medical prompts spanning 25 topics and 100 subtopics, an attack-defense pipeline over four MAS topologies, and a topology-aware personality screening and correction defense. The paper compares safety under baseline, attack, and defense conditions.

## Attack or Failure

### Attack Surface

Member-agent instructions and inter-agent medical deliberation.

### Attack Mechanism

A dark-personality insider injects harmful guidance that propagates or is aggregated by the MAS.

### System-Level Failure

The collective produces unsafe medical advice despite the presence of honest agents.

### Security Consequence

Loss of collective safety and decision integrity in a high-stakes domain.

## Defense

### Defense Mechanism

PCDC uses psychometric screening, behavioral verification, risk scoring, topology-aware isolation, and replacement or rehabilitation.

### Intervention Point

Membership, communication topology, and aggregation.

### Required Observability

Agent responses, risk scores, identity, and topology-specific routing context.

### Assumptions

An enforcement agent is trusted and can isolate, reweight, or replace risky members.

### Limitations

The paper studies four canonical topologies rather than hybrids; the defense uses fixed thresholds and rules; and the benchmark focuses on medical textual interaction.

## Evaluation

### Evaluated Systems

Medical MAS using GPT-4o, Claude-3.7, DeepSeek-V3, GPT-3.5-turbo, and Llama-family models in the reported analyses.

### Agent Configuration

Five agents under centralized, decentralized, layered, or shared-pool communication, with additional ablations over agent count, rounds, and dialogue length.

### Dataset or Environment

MedSentry's 5,000 harmful instructions; MedSafetyBench for comparison; MedQA and PubMedQA for utility validation.

### Baselines

Single-agent CoT and ReAct, MedPrompt, multi-expert prompting, and undefended versions of each topology.

### Metrics

Local Content Safety (LCS), Response Safety (RS), medical task accuracy, token usage, and evaluation time.

### Main Results

The reported attack degradation and defense recovery vary by topology; SharedPool is the most vulnerable in the main comparison and decentralized communication is the most resistant.

## Relation to Existing Work

### Papers Compared by the Authors

MedSafetyBench, MedAgentsBench, MedAgentBench, and medical multi-agent prompting methods.

### Claimed Research Gap

Medical safety benchmarks primarily assess single models or benign collaboration rather than insider threats across MAS architectures.

### Closest Related Work

Medical safety benchmarks and topology-aware MAS security studies.

### Difference From Prior Work

MedSentry combines a fine-grained adversarial medical dataset with controlled cross-topology attack and defense evaluation.

## Relevance to Our SoK

### Included Concepts

Insider threat, topology, propagation, global safety metrics, defense locus, and benchmark denominator.

### Taxonomy Implications

The same malicious-member mechanism produces topology-dependent collective outcomes, making architecture part of the evaluation contract.

### Supported Research Questions

How does communication structure alter insider-attack severity and defense recovery?

### Important Limitations

The work is arXiv-only: its ICLR 2026 record remains a submission rather than an accepted paper as of the access date.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| MedSentry contains 5,000 prompts covering 25 topics and 100 subtopics. | Explicit author claim | Paper | Abstract; 3 | 1; 4 | Table 1; Appendix Table 4 | Dataset composition. |
| The evaluation fixes five agents and compares four communication topologies. | Explicit author claim | Paper | 4; 5 | 5-7 | Figure 2; Table 3 | Cross-topology evaluation contract. |
| LCS and RS are the primary cross-topology safety metrics. | Explicit author claim | Paper | 4.2; 5 | 6-7 | Tables 2-3 | Metric definitions and results. |
| The ICLR record is not an accepted publication. | Metadata verification | OpenReview | Venue status | - | - | The record says Submitted to ICLR 2026, not Poster or Oral. |

## Provenance

### Discovery Source

arXiv; OpenReview publication-status audit; defense-artifact audit.

### Discovery Query

MedSentry multi-agent benchmark official publication

### Accessed Version

arXiv v1; ICLR 2026 submission status checked separately.

### Access Date

2026-08-06
### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-06
