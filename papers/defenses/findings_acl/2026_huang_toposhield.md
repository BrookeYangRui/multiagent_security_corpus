# TopoSHIELD: Reshaping the Flow of Malice via Spatio-Temporal Risk-Aware Topological Evolution in Multi-Agent Systems

## Citation
Title: TopoSHIELD: Reshaping the Flow of Malice via Spatio-Temporal Risk-Aware Topological Evolution in Multi-Agent Systems
Authors: Ruiyang Huang; Chenxi Wang; Tinghe Zhang; Fengrui Liu; Jiayan Sun; Haocheng Wang; Yifan Wu
Year: 2026
Venue: Findings of ACL
DOI: 10.18653/v1/2026.findings-acl.426
Primary URL: https://aclanthology.org/2026.findings-acl.426/
Open access URL: https://aclanthology.org/2026.findings-acl.426.pdf
BibTeX key: huang2026toposhield

## Paper Type
Defense; Evaluation; Empirical study

## Scope
### System Studied
LLM agents exchange messages over evolving communication graphs.
### Multi-Agent Dependency
Risk is estimated from temporal message flow and mitigated by editing graph edges and isolating risky communities.
### Application Domain
Collaborative reasoning under misinformation injection.

## Security Model
### Protected Assets
Collective answer integrity and benign-agent utility.
### Threat Actor
Malicious member agents injecting misinformation.
### Trusted Components
The spatio-temporal graph monitor and topology controller.
### Attacker Capabilities
Send persuasive malicious messages through allowed edges.
### Security Assumptions
Messages and topology are visible and edges can be pruned or communities isolated.

## Main Contribution
TopoSHIELD models interaction risk with a spatio-temporal graph neural network and evolves the topology using node-risk estimation and edge-attribution correction.

## Attack or Failure
### Attack Surface
Inter-agent communication edges.
### Attack Mechanism
Misinformation spreads from malicious nodes through repeated rounds.
### System-Level Failure
Graph-mediated propagation corrupts group conclusions.
### Security Consequence
Collective decision-integrity loss.

## Defense
### Defense Mechanism
Risk estimation, edge attribution, pruning, and community isolation.
### Intervention Point
Communication topology.
### Required Observability
Temporal message traces and the global graph.
### Assumptions
The defender can change the active topology during execution.
### Limitations
The paper notes that open, dynamic, and heterogeneous environments require further study.

## Evaluation
### Evaluated Systems
LLM-based multi-agent debate and reasoning systems, including GPT-4o settings.
### Agent Configuration
Multiple graph structures and attack placements.
### Dataset or Environment
Knowledge and reasoning tasks with injected misinformation.
### Baselines
Attack-only, static graph safeguards, and anomaly-detection baselines.
### Metrics
Toxicity or attack impact, task utility, and detection measures.
### Main Results
The authors report a 58% toxicity reduction on GPT-4o while retaining more than 90% utility in the highlighted setting.

## Relation to Existing Work
### Papers Compared by the Authors
G-Safeguard, BlindGuard, and graph anomaly methods.
### Claimed Research Gap
Static isolation does not account for time-varying propagation paths.
### Closest Related Work
Topology-guided MAS safeguards.
### Difference From Prior Work
TopoSHIELD treats topology as a dynamic defense action rather than only a detection feature.

## Relevance to Our SoK
### Included Concepts
Topology defense, temporal observability, propagation containment, and utility preservation.
### Taxonomy Implications
Defense locus is topology; functions are detection and containment.
### Supported Research Questions
Which interaction structures can be changed safely during defense?
### Important Limitations
The headline effect is setting-specific and not a universal guarantee.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| TopoSHIELD estimates temporal risk and edits topology. | Explicit author claim | Paper | 3-4 | 3-6 | Framework figure | Method pipeline. |
| The highlighted GPT-4o result reports 58% toxicity reduction and over 90% utility. | Explicit author claim | Paper | Abstract; 5 | 1; 7-10 | Results tables | Author-reported result. |
| Defense requires global graph and trace access. | Corpus interpretation | Paper | 3-4 | 3-6 | Framework figure | Required model inputs and actions. |

## Provenance
### Discovery Source
ACL Anthology; prior corpus defense scan.
### Discovery Query
TopoSHIELD official Findings ACL
### Accessed Version
Published Findings of ACL 2026 version.
### Access Date
2026-08-06
### Prepared By
Human or automated process: automated extraction
Model and version, if automatically generated: Not recorded
### Verification Status
agent_unverified
### Last Updated
2026-08-06
