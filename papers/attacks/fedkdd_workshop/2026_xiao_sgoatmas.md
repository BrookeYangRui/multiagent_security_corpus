# You Don't Have to Be the One Doing Evil! Locate a Scapegoat within Multi-Agent Systems for Executing Covert Attacks

## Citation

Title: You Don't Have to Be the One Doing Evil! Locate a Scapegoat within Multi-Agent Systems for Executing Covert Attacks

Authors: Tianzhe Xiao; Haozhao Wang; Yichen Li; Tianlong Luo; Xiong Yongfu; Daiming Kuang; Yi Wang; Yi Liu; Ruixuan Li

Year: 2026

Venue: FedKDD/FedMAS Workshop

DOI: Not reported

Primary URL: https://openreview.net/forum?id=CIRI47rmLQ

Open access URL: https://openreview.net/pdf?id=CIRI47rmLQ

BibTeX key: xiao2026sgoatmas

## Paper Type

Attack; Evaluation; Empirical study

## Scope

### System Studied

LLM-backed workflows using hierarchical, centralized, and decentralized communication over knowledge, mathematics, and code tasks.

### Multi-Agent Dependency

A malicious member manipulates a downstream honest agent into producing the sabotaging output, shifting observable attribution away from the attacker.

### Application Domain

Question answering, mathematical reasoning, and code generation.

## Security Model

### Protected Assets

Collective task correctness and accountability for malicious influence.

### Threat Actor

One malicious member at a selectable position in the workflow.

### Trusted Components

Task labels, attack evaluator, and external detection procedure.

### Attacker Capabilities

The member observes its workflow context, sends a crafted logic-based payload, and selects an attack edge using system structure.

### Security Assumptions

The attacker operates through ordinary messages and seeks both performance degradation and low attribution risk.

## Main Contribution

SGoatMAS models the workflow as a system-level chain of thought and uses Vulnerability-to-Risk Ratio (VRR) to choose an attack point. Its scapegoating attack induces another agent to emit the harmful contribution, trading off degradation against detectability.

## Attack or Failure

### Attack Surface

Inter-agent reasoning links, role position, and aggregation paths.

### Attack Mechanism

Reconnaissance reconstructs the workflow, VRR selects a target edge, and a covert payload steers a downstream scapegoat toward an incorrect contribution.

### System-Level Failure

The final system answer is corrupted while monitoring attributes the suspicious output to an honest downstream agent.

### Security Consequence

Loss of collective decision integrity and reliable attribution.

## Defense

### Defense Mechanism

Not proposed; an external detector is used to measure attack visibility.

### Intervention Point

Not applicable.

### Required Observability

Evaluation observes messages, agent positions, the final answer, and detector decisions.

### Assumptions

Detection Rate is specific to the evaluated detector and does not establish general undetectability.

### Limitations

The study uses three workflow families, five datasets, small populations, and generated payloads; results do not establish real-world prevalence.

## Evaluation

### Evaluated Systems

LLM multi-agent workflows over MMLU, MMLU-Pro, GSM8K, Arithmetic, and HumanEval.

### Agent Configuration

Hierarchical, centralized, and decentralized workflows, with malicious position varied and decentralized size scaled from two to four agents.

### Dataset or Environment

Five established reasoning and code benchmarks adapted to the attack protocol.

### Baselines

Benign execution and a naive direct attack.

### Metrics

Final system Accuracy, Detection Rate, Scapegoat Accuracy, and VRR for target selection.

### Main Results

SGoatMAS generally reduces system accuracy with lower detection and higher scapegoat attribution than the naive baseline; effects vary materially by topology and attacker position.

## Relation to Existing Work

### Papers Compared by the Authors

Direct malicious-member attacks, topology-aware attacks, and integrity attacks on LLM-MAS.

### Claimed Research Gap

Prior attacks are directly attributable to the malicious sender and do not optimize which honest member appears responsible.

### Closest Related Work

Demonstrations of Integrity Attacks in Multi-Agent Systems and topology-guided propagation attacks.

### Difference From Prior Work

The attack jointly optimizes task damage and attribution risk through structural reconnaissance.

## Relevance to Our SoK

### Included Concepts

Malicious member, topology, adversary position, covert influence, attribution, and measurement contract.

### Taxonomy Implications

Scapegoating is an attack mechanism that produces collective decision-integrity and oversight failures, not a separate system-level property.

### Supported Research Questions

How do topology and adversary position affect attack impact and observability?

### Important Limitations

The accepted workshop version is canonical; the earlier anonymous ICLR submission is not counted separately.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| SGoatMAS uses VRR to select a covert attack point in the workflow. | Explicit author claim | Paper | 4 | 4-6 | Figure 1 | Attack pipeline. |
| Evaluation crosses three topologies and five datasets. | Explicit author claim | Paper | 5 | 7-9 | Tables 1-2 | Evaluation matrix. |
| Metrics are system Accuracy, Detection Rate, and Scapegoat Accuracy. | Explicit author claim | Paper | 5 | 7-8 | Tables 1-2 | Metric contract. |
| The paper is a FedKDD/FedMAS 2026 Oral. | Metadata verification | OpenReview | Venue status | - | - | Public accepted record. |

## Provenance

### Discovery Source

OpenReview benchmark-name reverse search; publication-status reconciliation.

### Discovery Query

SGoatMAS multi-agent security benchmark

### Accessed Version

FedKDD/FedMAS 2026 Oral version.

### Access Date

2026-08-06
### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-06
