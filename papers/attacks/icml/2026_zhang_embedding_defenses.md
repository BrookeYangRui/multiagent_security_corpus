# When Embedding-Based Defenses Fail: Rethinking Safety in LLM-Based Multi-Agent Systems

## Citation

Title: When Embedding-Based Defenses Fail: Rethinking Safety in LLM-Based Multi-Agent Systems

Authors: Lingxi Zhang; Guangtao Zheng; Hanjie Chen

Year: 2026

Venue: ICML

DOI: Not reported

Primary URL: https://icml.cc/virtual/2026/poster/62170

Open access URL: https://arxiv.org/abs/2605.01133

BibTeX key: zhang2026embeddingdefenses

## Paper Type

- Attack
- Defense
- Evaluation
- Empirical study
- Theoretical analysis

## Scope

### System Studied

LLM multi-agent reasoning systems using star, chain, or sparse-random communication and embedding-based graph defenses.

### Multi-Agent Dependency

A compromised member repeatedly sends messages that are propagated, echoed, and aggregated by other agents. The attacks specifically manipulate separation between malicious and benign communication embeddings over rounds and topologies.

### Application Domain

Collaborative knowledge and reasoning tasks.

## Security Model

### Protected Assets

Integrity of the final group decision and reliable attribution or pruning of malicious members.

### Threat Actor

One compromised member agent.

### Trusted Components

Benign agents, the experiment controller, message-defense implementation, and access to token probabilities or logits for the proposed defense.

### Attacker Capabilities

The compromised agent generates protocol-valid misinformation and adapts its text to remain close to benign embeddings or to increase benign-message dispersion.

### Security Assumptions

The attacker can shape message wording but does not alter the defense code or other agents' internal states; token-level confidence remains available at generation time.

## Main Contribution

The paper analyzes a broad acceptance-region failure of embedding detectors and instantiates three near-benign attacks: Slow Drift, Benign Wrapper, and Chaos Seeding. It proposes confidence-guided pruning and weighting based on token uncertainty and measures how both defensive signals decay over communication rounds.

## Attack or Failure

### Attack Surface

Protocol-valid inter-agent text and embedding-based graph anomaly detection.

### Attack Mechanism

Slow Drift changes claims gradually, Benign Wrapper dominates the malicious payload with benign context, and Chaos Seeding makes benign agents disagree so malicious messages cease to be embedding outliers.

### System-Level Failure

Embedding defenses retain attacker messages, which propagate and steer the final group answer.

### Security Consequence

Collective decision-integrity failure and loss of reliable malicious-member attribution.

## Defense

### Defense Mechanism

Confidence pruning blocks low-confidence messages; confidence weighting attaches token-uncertainty metadata and reduces uncertain messages' influence during aggregation.

### Intervention Point

Message propagation and collective aggregation.

### Required Observability

The defense needs per-message token probabilities or logits before messages are echoed and mixed through the graph.

### Assumptions

Malicious generation has a separable token-confidence signal even when its final text embedding is near benign communication.

### Limitations

Both embedding and confidence signals decay after repeated propagation, especially in dense topologies; API models may expose only limited token probabilities, and adaptive attacks against the confidence signal are not established as covered.

## Evaluation

### Evaluated Systems

Llama-3.1-8B, Qwen3-4B, and GPT-4o-mini with no defense, G-Safeguard, GUARDIAN, or confidence-guided filtering.

### Agent Configuration

Star, chain, and sparse-random directed graphs under multi-round communication.

### Dataset or Environment

Subsets of MMLU, GSM8K, and BBH.

### Baselines

No defense and the embedding/graph defenses G-Safeguard and GUARDIAN.

### Metrics

Majority-vote or exact-match accuracy, attack success rate, embedding distances, malicious-agent AUROC, signal half-life, and area under the AUROC-by-round curve.

### Main Results

The three near-benign attacks reduce embedding separability and degrade the tested embedding defenses; confidence-guided filtering recovers more task accuracy in the reported settings, but its attribution signal also decays over rounds.

## Relation to Existing Work

### Papers Compared by the Authors

G-Safeguard, GUARDIAN, NetSafe, communication attacks, and confidence-estimation methods.

### Claimed Research Gap

Existing graph defenses were evaluated mainly against conspicuous malicious messages that remain embedding outliers.

### Closest Related Work

G-Safeguard and GUARDIAN.

### Difference From Prior Work

The attacks optimize the assumptions of embedding separation itself, while the proposed defense uses generation-time token confidence rather than only final-text geometry.

## Relevance to Our SoK

### Included Concepts

Compromised member, adaptive defense evasion, message embedding, token confidence, topology density, propagation rounds, early intervention, and attribution decay.

### Taxonomy Implications

Near-benign wording is an attack mechanism against a detector; the resulting property violation is collective decision integrity, while topology controls the time window for defense.

### Supported Research Questions

Are defenses evaluated against adaptive attacks, what metadata do they require, and how does observer signal quality change over interaction rounds?

### Important Limitations

The experiments sample three reasoning datasets and three model backbones; results do not establish that confidence is robust to a fully adaptive attacker optimizing against both signals.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| Slow Drift, Benign Wrapper, and Chaos Seeding target distinct embedding-separation assumptions. | Explicit author claim | Paper | 5 | 4-5 | Figure 2 | Attack definitions. |
| Confidence pruning and weighting use token-level uncertainty. | Explicit author claim | Paper | 6 | 5-6 | - | Defense definitions. |
| Three datasets, three models, and three topology families are evaluated. | Explicit author claim | Paper | 7.1 | 6 | - | Experimental setup. |
| G-Safeguard and GUARDIAN degrade under near-benign attacks in the reported results. | Explicit author claim | Paper | 7.2 | 6-7 | Tables 1 and 3 | Defense comparison. |
| Embedding and confidence signals decay faster in denser graphs. | Explicit author claim | Paper | 8 | 7-8 | Tables 4-5 | Signal-persistence analysis. |

## Provenance

### Discovery Source

ICML official program; arXiv; prior corpus completeness scan.

### Discovery Query

`site:icml.cc/Downloads/2026 multi-agent security embedding defense`

### Accessed Version

Published ICML paper; full text accessed as arXiv v3 because the PMLR page was not yet indexed.

### Access Date

2026-08-05

### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-05

