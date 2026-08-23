# Explainable and Fine-Grained Safeguarding of LLM Multi-Agent Systems via Bi-Level Graph Anomaly Detection

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set1_core` · `defense` · venue `ACL` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation
Title: Explainable and Fine-Grained Safeguarding of LLM Multi-Agent Systems via Bi-Level Graph Anomaly Detection
Authors: Junjun Pan; Yixin Liu; Rui Miao; Kaize Ding; Yu Zheng; Quoc Viet Hung Nguyen; Alan Wee-Chung Liew; Shirui Pan
Year: 2026
Venue: ACL
DOI: 10.18653/v1/2026.acl-long.1407
Primary URL: https://aclanthology.org/2026.acl-long.1407/
Open access URL: https://aclanthology.org/2026.acl-long.1407.pdf
BibTeX key: pan2026xgguard

## Paper Type
Defense; Evaluation; Empirical study

## Scope
### System Studied
Communicating LLM agents arranged as chain, tree, star, or random graphs.
### Multi-Agent Dependency
The detector uses both response-level signals and graph neighborhoods, and remediation removes malicious nodes from the communication topology.
### Application Domain
Collaborative reasoning, tool use, and memory-augmented question answering.

## Security Model
### Protected Assets
Collective answer integrity and propagation containment.
### Threat Actor
Compromised member agents.
### Trusted Components
The graph monitor, response encoder, and remediation controller.
### Attacker Capabilities
Prompt, tool-output, or memory poisoning that changes agent messages.
### Security Assumptions
The defender observes responses and graph edges and can isolate nodes.

## Main Contribution
XG-Guard combines fine-grained lexical explanations with a bi-level graph anomaly detector. It identifies malicious responses and agents, then removes detected agents from the graph.

## Attack or Failure
### Attack Surface
Agent inputs, memory, tools, and inter-agent messages.
### Attack Mechanism
Compromised members introduce misleading content that propagates through collaboration.
### System-Level Failure
Contagion corrupts the collective answer.
### Security Consequence
Loss of collective decision integrity.

## Defense
### Defense Mechanism
Response-level explanation and graph-level anomaly detection followed by topology repair.
### Intervention Point
Messages and communication topology.
### Required Observability
Agent responses, node identities, and graph neighborhoods.
### Assumptions
Normal traces are available and the controller can remove agents.
### Limitations
The paper studies fixed synthetic topologies and three attack families; adaptive evasion and open membership remain outside the evaluation.

## Evaluation
### Evaluated Systems
GPT-4o-mini, DeepSeek-V3, and Qwen-family MAS configurations.
### Agent Configuration
Four topology families with multi-round communication.
### Dataset or Environment
CSQA, MMLU, GSM8K, InjecAgent, and memory-poisoning tasks.
### Baselines
DOMINANT, PREM, TAM, BlindGuard, and G-Safeguard.
### Metrics
AUROC, attack success rate, and answer accuracy.
### Main Results
The authors report stronger unsupervised detection and post-remediation utility than the unsupervised baselines across evaluated settings.

## Relation to Existing Work
### Papers Compared by the Authors
BlindGuard, G-Safeguard, and graph anomaly detectors.
### Claimed Research Gap
Prior safeguards either require labels or lack fine-grained explanations.
### Closest Related Work
BlindGuard and G-Safeguard.
### Difference From Prior Work
XG-Guard jointly localizes suspicious text and graph-level actors.

## Relevance to Our SoK
### Included Concepts
Topology-aware detection, explainability, containment, and global observability.
### Taxonomy Implications
Defense locus is message plus topology; functions are detection and containment.
### Supported Research Questions
What graph visibility and intervention rights do MAS defenses assume?
### Important Limitations
Reported robustness is empirical rather than a guarantee against adaptive attackers.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| XG-Guard uses response- and graph-level anomaly detection followed by node removal. | Explicit author claim | Paper | 3 | 3-6 | Figure 2 | Architecture and remediation workflow. |
| Evaluation covers three attack surfaces and four topologies. | Explicit author claim | Paper | 4.1 | 6 | Table 1 | Experimental setup. |
| The method requires graph-wide response visibility. | Corpus interpretation | Paper | 3 | 3-6 | Figure 2 | Inputs required by both detector levels. |

## Provenance
### Discovery Source
ACL Anthology; prior corpus defense scan.
### Discovery Query
XG-Guard multi-agent official ACL
### Accessed Version
Published ACL 2026 version.
### Access Date
2026-08-06
### Prepared By
Human or automated process: automated extraction
Model and version, if automatically generated: Not recorded
### Verification Status
agent_unverified
### Last Updated
2026-08-06
